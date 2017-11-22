from math import log
import operator
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
    labels = ['no surfacing','flippers']
    return dataSet,labels

def splitDataSet(dataSet,axis,value):
    """
    Args:
        其中dataSet是要处理的数据集,axis是要处理的第几个维度，value是给定的特征
    return：
        返回的将是符合特征的数据集的子集
    """
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis]==value:
            reducedFearVec = featVec[:axis]
            reducedFearVec.extend(featVec[axis+1:])#extend可以理解为是合并
            retDataSet.append(reducedFearVec)#append是添加一个元素
    return retDataSet

def chooseBestFeaturesToSplit(dataSet):
    """
    这个函数用于选择最好的特征值
    """
    numFeatures = len(dataSet[0]) -1#特征的个数
    baseEntropy =calcShanonEnt(dataSet)#计算最初的信息熵
    bestInfoGain =0.0
    bestFeature = -1
    for i in list(range(numFeatures)):
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet,i,value)
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy+=prob*calcShanonEnt(subDataSet)
            infoGain = baseEntropy-newEntropy#大于零的意思是说这个信息熵在减少
            if(infoGain > bestInfoGain):
                bestInfoGain = infoGain
                bestFeature = i
        return bestFeature

def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():classCount[vote]= 0
        classCount[vote] +=1
    sortedClassCount = sorted(classCount.items(),key=operator.items(1),reverse = True)
    return sortedClassCount[0][0]



def creatTree(dataSet,labels):
    """
    Args:
        dataSet是数据集合
        labels是属性说明
    伪代码如下：
        if 数据集合中只要一类
            结束
        if 使用完了所有的数据
            结束
        从当前数据集中选择最好的分类属性
        选择当前数据集合中最好的分类属性,labels是属性说明
        bestFeatLabel=找出最好的属性
        表示树：myTree = {bestFeatLabel:{}}，这里是通过dict来表示一棵树的，
        然后被最好分类属性的取值放在一个数组里，featValues
        然后分割数据集，构造子树，其中上面有几个属性值就循环几次

    """
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0])==len(classList):#类别完全相同就停止划分
        return classList[0]
    if len(dataSet[0]) ==1:
        return majorityCnt(classList)
    bestFeat = chooseBestFeaturesToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]
        myTree[bestFeatLabel][value]=creatTree(splitDataSet(dataSet,bestFeat,value),subLabels)
    return myTree