# -*- coding: UTF-8 -*-
import time
from functools import wraps


def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print ("Total time running %s: %s seconds" %
               (function.func_name, str(t1 - t0))
               )
        return result
    return function_timer


class Node:
    def __init__(self, name, num, parent):
        self.name = name
        self.num = num
        self.parent = parent
        self.children = {}

    def add(self, num):
        self.num += num


@fn_timer
def getFormatData():
    formatData = []
    Data = open("retail.dat", 'r')
    for line in Data:
        formatData.append([int(i) for i in line.split()])

    return formatData


# @fn_timer
def getFirstData(formatData):
    dic = {}
    numDict = {}
    headDict = {}
    newData = {}
    for line in formatData:
        for item in line:
            numDict[item] = numDict.get(item, 0) + 1
    for line in formatData:
        # line.sort(key=lambda item: numDict[item])
        newLine = []
        for item in line:
            if numDict[item] >= minSupport:
                newLine.append(item)
                dic[item] = numDict[item]
                headDict[item] = []
        if len(newLine) > 0:
            newLine = frozenset(newLine)
            newData[newLine] = newData.get(newLine, 0) + 1
    return newData, dic, headDict


def getNewData(formatData):
    dic = {}
    numDict = {}
    headDict = {}
    newData = {}
    for line, num in formatData.items():
        for item in line:
            numDict[item] = numDict.get(item, 0) + num
    for line, num in formatData.items():
        newLine = []
        for item in line:
            if numDict[item] >= minSupport:
                newLine.append(item)
                dic[item] = numDict[item]
                headDict[item] = []
        if len(newLine) > 0:
            newData[frozenset(newLine)] = newData.get(
                frozenset(newLine), 0) + num
            # newData[frozenset(newLine)] = num

    return newData, dic, headDict


def findFreq(headDict, oldNumDict, lastRes):  # res = []
    a = sorted(oldNumDict.items(), key=lambda item: (
        item[1], item[0]), reverse=True)
    for key, value in a:
        nodeList = headDict[key]
        temp = lastRes[:]
        temp.append(key)
        result[frozenset(temp)] = oldNumDict[key]
        formatData = creatFormatData(nodeList)
        if len(formatData) != 0:
            newData, numDict, newHeadDict = getNewData(formatData)
            if len(newData) == 0:
                continue
            retNode, newHeadDict = creatTree(newData, newHeadDict, numDict)

            findFreq(newHeadDict, numDict, temp)
    return


def creatFormatData(nodeList):
    newData = {}
    for node in nodeList:
        line = []
        num = node.num
        node = node.parent
        while node.name != 'Null':
            line.append(node.name)
            node = node.parent
        if len(line) > 0:
            newData[frozenset(line)] = num
    return newData


# @fn_timer
def creatTree(newData, headDict, numDict):
    retNode = Node('Null', 1, None)
    for line, num in newData.items():
        line = list(line)
        line.sort(key=lambda item: (numDict[item], item), reverse=True)
        insertNode(line, retNode, headDict, num)
    return retNode, headDict


# @fn_timer
def insertNode(line, parentNode, headDict, num):
    item = line[0]
    if item in parentNode.children:
        parentNode.children[item].add(num)
    else:
        newNode = Node(item, num, parentNode)
        parentNode.children[item] = newNode
        headDict[item].append(newNode)
    if len(line) > 1:
        insertNode(line[1:], parentNode.children[item], headDict, num)
    return


result = {}
# 总共88162条数据
minSupport = 881  # 检查作业要求最小支持度用数量来表示
# 4410
# 881
# 441


@fn_timer
def main():
    formatData = getFormatData()
    newData, numDict, headDict = getFirstData(formatData)

    retNode, headDict = creatTree(newData, headDict, numDict)

    findFreq(headDict, numDict, [])
    formatRes = {}
    for item, num in result.items():
        length = len(item)
        a = formatRes.get(length, 0)
        if a != 0:
            formatRes[length][item] = num
        else:
            formatRes[length] = {item: num}
    # a = []
    sum = 0
    for num, item in formatRes.items():
        print('%d项集个数：%d' % (num, len(item))),
        print('--------------------')
        sum += len(item)
        # for k, v in item.items():
        #     print(list(k), v),
        #     # a.append((k))
        #     print('.')
    # print(a)
    print('总共%d个' % sum)


main()
