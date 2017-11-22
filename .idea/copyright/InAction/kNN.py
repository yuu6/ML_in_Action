from numpy import *
import operator
##首先创造数据集
def createDataset():
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return group ,labels

#这是k近邻算法

def classify0(inX,dataSet,labels,k):#inX是要测试的数据，dataset是训练的数据集，labels是标签，K是k近邻的意思
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX,(dataSetSize,1))-dataSet
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)#这里的求和指的是每一行求和
    distances = sqDistances**0.5
    sortedDistIndicies = distances.argsort()#排序完成的结果是下标
    classCount ={}#这是一个字典类型
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel,0)+1
    sortedClassCount = sorted(classCount.items(),key=operator.itemgetter(1),reverse = True)
    return sortedClassCount[0][0]

#将文件记录转化为Numpy的解析程序
def file2matrix(filename):
    fr = open(filename)
    arrayLines = fr.readlines()#这个函数将文件一起读入内存
    numberOfLines =len(arrayLines)#得到文件的总行数
    returnMat = zeros((numberOfLines,3))#创建全零的数组
    classLabelVector = []
    index = 0
    for line in arrayLines:
        line = line.strip()
        listFormLine = line.split("\t")#使用制表符分割这个字符串
        returnMat[index,:] = listFormLine[0:3]#0:3应该不包括3
        classLabelVector.append(int(listFormLine[-1]))#这里的-1是倒数第一个
        index +=1
    return returnMat,classLabelVector
    #返回矩阵以及标签数组


#下面的函数将会对数据进行归一化

def autoNorm(dataset):
    minVals = dataset.min(0)#这里的0表示每一列的
    maxVals = dataset.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataset))
    m = dataset.shape[0]
    normDataSet = dataset - tile(minVals,(m,1))#这里的tile应该翻译为铺砖
    normDataSet = normDataSet/tile(ranges,(m,1))#这里的除指的是特征值相除
    return normDataSet,ranges,minVals
#下面的函数用于训练以及训练结果的计算
def datingClassTest():
    hoRatio = 0.10
    datingDataMat,datingLabels = file2matrix('datingTestSet2.txt')#首先读数据
    normMat,ranges,minVals = autoNorm(datingDataMat)#数据归一化,这里的 ranges一定不要写错了，写成range是我之前的错误
    m = normMat.shape[0]#这个是总的行数
    numTestVecs = int(m*hoRatio)#这个是测试集的个数
    print(type(numTestVecs),m)
    errorCount = 0.0
    trainMat= normMat[numTestVecs:m,:]#这个就是总的训练集
    trainLabels = datingLabels[numTestVecs:m]#这个就是训练样本
    for i in list(range(numTestVecs)):
        print(i)
        classifierResult = classify0(normMat[i,:],trainMat,trainLabels,3)#调用分类函数
        print ("the classifier came back with: %d ,the real answer is:%d"% (classifierResult,datingLabels[i]))
        if(classifierResult !=datingLabels[i]):errorCount +=1.0
    print ("the total error is :%f"%(errorCount/float(numTestVecs)))#计算最终的失误率
    print (errorCount)

def classifyPerson():
    resultList = ['not at all','in small doses','in large doses']
    percentTats = float(input("percentage of time spent playing video games?"))#实际输入的值
    ffMiles =float(input("frequent flier miles earned per year?"))
    iceCream = float(input("liters of ice cream consumed per years"))
    datingDataMat,datingLabels = file2matrix('datingTestSet2.txt')
    normMat ,ranges,minVals = autoNorm(datingDataMat)
    inArr =array([ffMiles,percentTats,iceCream])
    classifierResult = classify0((inArr-minVals)/ranges,normMat,datingLabels,3)
    print("you will probably like this person:",resultList[classifierResult-1])