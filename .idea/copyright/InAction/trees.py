from math import log

'''
calcShanonEnt函数主要是计算信息熵
'''
def calcShanonEnt(dataSet):
    """
    Args:
        dataSet是要测试的数据集
    return：
        返回的是信息熵
    """
    numEntries =len(dataSet)#dataset是一个list
    labelCounts={}#存储每个类别的数目
    for featVec in dataSet:#featVec是每一条数据
        currentLabels = featVec[-1]#标签位于每一条数据的最后一个位置
        if currentLabels not in labelCounts.keys():
            labelCounts[currentLabels] =0
        labelCounts[currentLabels] +=1
        shannonEnt = 0.0
    for key in labelCounts:
        prob =float(labelCounts[key])/numEntries#计算每一类可能出现的概率
        shannonEnt -=prob*log(prob,2)
    return shannonEnt#最终算出来的及时信息熵函数

def creatDataSet():
    """
    产生数据集合
    """
    dataSet = [[1,1,'yes'],
               [1,1,'yes'],
               [1,0,'no'],
               [0,1,'no'],
               [0,1,'no']]
    labels = ['no surfacing',flippers]
    return dataSet,labels