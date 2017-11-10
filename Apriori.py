# -*- coding: UTF-8 -*-
import time
from functools import wraps
from itertools import combinations


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


@fn_timer
def getFormatData():
    formatData = []
    Data = open("retail.dat", 'r')
    for line in Data:
        formatData.append(set([int(i) for i in line.split()]))
    # return formatData[0:10000]
    return formatData


@fn_timer
def checkFirstSet(formatData, minSupport):
    numDict = {}
    supportSet = set()
    for line in formatData:
        for item in line:
            numDict[item] = numDict.get(item, 0) + 1
            if numDict[item] >= minSupport:
                supportSet.add(frozenset([item]))
    return list(supportSet)


@fn_timer
def getSecondSet(Set):

    length = len(Set)
    newSet = set()
    for item1 in range(length):
        for item2 in range(item1 + 1, length):
            newSet.add(Set[item1] | Set[item2])
    return list(newSet)


@fn_timer
def getNewSet(Set, k):

    length = len(Set)
    newSet = set()
    for item1 in range(length):
        for item2 in range(item1 + 1, length):
            if(sorted(list(Set[item1]))[:k - 2] == sorted(list(Set[item2]))[:k - 2]):
                unionSet = Set[item1] | Set[item2]
                subset = list(combinations(unionSet, k - 1))
                for i in subset:
                    if set(i) not in Set:
                        break
                else:
                    newSet.add(unionSet)
    return list(newSet)


@fn_timer
def checkNewSet(formatData, newSet, minSupport):
    numDict = {}  # dic 键为item值为重复多少次
    supportSet = set()  # 支持度大于最小支持度的单项元素集合
    if len(newSet) > 0:
        for line in formatData:
            item = 0
            while item < len(newSet):
                if line >= newSet[item]:  # 判断item是否为line的子集
                    numDict[newSet[item]] = numDict.get(newSet[item], 0) + 1
                    if numDict[newSet[item]] >= minSupport:
                        supportSet.add(newSet[item])
                        newSet.remove(newSet[item])
                    else:
                        item += 1
                else:
                    item += 1

    return list(supportSet)


@fn_timer
def main():
    formatData = getFormatData()

    # 总共88162条数据
    minSupport = 881  # 检查作业要求最小支持度用数量来表示
    # 4410
    # 881
    # 441

    supportSet = checkFirstSet(formatData, minSupport)
    resSet = [supportSet]
    k = 2
    newSet = getSecondSet(resSet[k - 2])
    newNupportSet = checkNewSet(formatData, newSet, minSupport)
    resSet.append(newNupportSet)
    k += 1
    while(len(resSet[k - 2]) > 0):
        newSet = getNewSet(resSet[k - 2], k)
        newNupportSet = checkNewSet(formatData, newSet, minSupport)
        resSet.append(newNupportSet)
        k += 1

    resSet = resSet[:-1]
    sum = 0

    for line in resSet:
        for item in line:
            print(list(item)),
        print('')
        print('%d项集个数：%d' % (len(item), len(line))),
        print('-----------------------------------------------------')
        sum += len(line)
    print('总共%d个' % sum)


if __name__ == '__main__':
    main()
