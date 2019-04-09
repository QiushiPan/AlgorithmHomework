import random
import numpy as np
import time
import matplotlib.pyplot as plt
import math

Node = []
NodeList = []
Edge = []

CostTime = 0
nlogn = []

# 优化后的比较方法
def Compare(Left, Right, x):
    """
    将目标点与边的位置作对比，主要目的是得到点在边的上方和下方，如果碰到其他异常情况，也会返回结果。
    :param Left: 原线段左节点。
    :param Right: 原线段右节点。
    :param x: 目标节点坐标。
    :param State: 0，在下方；1，在上方；2，横轴坐标值越界；3，其他异常。
    :return: 点与边的位置关系，和点到边的纵轴截距。
    """
    LeftNode = Node[Left]
    RightNode = Node[Right]
    if(LeftNode[0] == RightNode[0]):
        return 3, 0
    TargetNode = Node[x]
    if (TargetNode[0] >= RightNode[0] or TargetNode[0] <= LeftNode[0]):
        return 2, 0
    LeftDiff = TargetNode[0] - LeftNode[0]
    RightDiff = RightNode[0] - TargetNode[0]
    AllDiff = LeftDiff + RightDiff
    ReferHigh = RightNode[1] * LeftDiff / AllDiff + LeftNode[1] * RightDiff / AllDiff
    ReferVal = TargetNode[1] - ReferHigh
    if(ReferVal < 0) :
        ResultState = 0
    elif(ReferVal > 0) :
        ResultState = 1
    else:
        ResultState = 3  # 相等

    return ResultState, ReferVal  # 返回比较状态结果和距离

# 原比较方法
# def Compare(Left, Right, x):
#     """
#     将目标点与边的位置作对比，主要目的是得到点在边的上方和下方，如果碰到其他异常情况，也会返回结果。
#     :param Left: 原线段左节点。
#     :param Right: 原线段右节点。
#     :param x: 目标节点坐标。
#     :param State: 0，在下方；1，在上方；2，横轴坐标值越界；3，其他异常。
#     :return: 点与边的位置关系，和点到边的纵轴截距。
#     """
#     LeftNode = Node[Left]
#     RightNode = Node[Right]
#     if(LeftNode[0] == RightNode[0]):
#         return 3, 0
#     TargetNode = Node[x]
#     ReferVal = LeftNode[0]*RightNode[1]+TargetNode[0]*LeftNode[1]+RightNode[0]*TargetNode[1]-LeftNode[0]*TargetNode[1]-RightNode[0]*LeftNode[1]-TargetNode[0]*RightNode[1]
#     if(ReferVal < 0) :
#         ResultState = 0
#     elif(ReferVal > 0) :
#         ResultState = 1
#     else:
#         ResultState = 3  # 相等
#
#     return ResultState, ReferVal  # 返回比较状态结果和距离
#
def FindNode(Left, Right, Candidate, state):
    """
    处理一条边，根据state参数，寻找一条边上方或下方的所有点，并且找出距离最远的一个点。
    :param Left: 原线段左节点下标
    :param Right: 原线段右节点下标
    :param Candidate: 待比较的节点集合
    :param state: 比较的目标：0，找线下方的点，1，找线上方的点
    :return: 距离最远的点的编号，所有符合条件的点的编号集合
    """
    CheckNode = []
    Distance = []
    for i in range(len(Candidate)):
        Result, distan = Compare(Left, Right, Candidate[i])
        if( Result == state ):
            CheckNode.append(Candidate[i])
            Distance.append(distan)

    if(len(CheckNode) == 0):
        return -1, 0 # 没有合适的点

    if( state == 1 ):
        ResultNode = np.argmax(Distance, axis=0)
    elif( state == 0 ):
        ResultNode = np.argmin(Distance, axis=0)

    # 返回距离最远的点的下标
    return CheckNode[ResultNode], CheckNode

def ProcessLine(Left, Right, NodeList, state):
    """
    处理一条线的上方或者下方。
    如果一条边的外边存在点，删除这条线，并且加入两条新的边。
    递归调用，处理两条新的边。
    :param Left: 边的左端点
    :param Right: 边的右端点
    :param state: 根据上土堡还是下凸包，寻找边上方或下方是否存在点
    """

    Edge.append([Left, Right])
    MedNode, CanNode = FindNode(Left, Right, NodeList, state)
    if(MedNode != -1):
        CanNode.remove(MedNode)
        Edge.remove([Left, Right])
        ProcessLine(Left, MedNode, CanNode, state)
        ProcessLine(MedNode, Right, CanNode, state)


def QuickHull(Nodes):
    global Node
    global NodeList
    global Edge
    Node = Nodes
    NodeList = []
    Edge = []
    for i in range(len(Nodes)):
        # Node.append([random.randint(0, 500), random.randint(0, 500)])
        NodeList.append(i)
    time_start = time.time()
    # 第一条线竖直画，第一次求出的两点分别是横坐标最大和最小的两点
    max_x = np.argmax(Node, axis=0)[0]
    min_x = np.argmin(Node, axis=0)[0]
    NodeList.remove(max_x)
    NodeList.remove(min_x)

    # 分别处理上凸包和下凸包
    ProcessLine(min_x, max_x, NodeList, 1)
    ProcessLine(min_x, max_x, NodeList, 0)

    time_end = time.time()
    CostTime = time_end - time_start

    return Edge, CostTime