import pandas as pd 
import math
import json
import pydot
#find the attribute to split at current level
def findIndex(attributeList):
    global attributeIndex
    for s in attributeList:
        if attributeDict[s]==min(attributeDict.values()):
            attributeIndex = s
    splitList.append(attributeIndex)
#save attribute and its entropy in a dictionary
def entropyCalculator(listCalculated, sampleBase):
    global attributeDict
    attributeDict = {}
    for k in listCalculated:
        #classes of each attribute
        attributeClass=samplePool[k].unique()
        attributeEntropy=0
        #calculate entropy
        for v in attributeClass:
            Vclass=sampleBase[samplePool[k]==v]
            Vseries=Vclass.value_counts()
            attributeClassEntropy=sum(math.log2(n/sum(Vseries))*(-n/sum(Vseries)) for n in Vseries)
            attributeEntropy += attributeClassEntropy*Vclass.count()/len(sampleBase)
        #save attribute and its entroy in a dictionary
        attributeDict[k]=attributeEntropy
    return attributeDict
#remove the attribute found at the last level
def removeAttribute(sourceList, spliteOrder):
    targetList = sourceList[:]
    try:
        targetList.remove(splitList[spliteOrder])
    except ValueError:
        targetList = targetList
    return targetList
#You can customize file aame, rows to read and columns to read
fileName = 'C:/Fordham/Fall 2019/Data Mining/Homework/HW2/data files for HW 2 decision trees/example.csv'
rowsRead = 100
columnsRead = [0,1,2,3,4]
samplePool = pd.read_csv(fileName, nrows=rowsRead, usecols=columnsRead)
columnList = list(samplePool)
attributeList = list(samplePool)
del attributeList[-1]
#save the attributes to split in a list by order
splitList = ['index']
treeDict={}
treeDict1={}
attributeDict={}
for i in attributeList:
    #classes of each attribute
    attributeClass1=samplePool[i].unique()
    attributeEntropy1=0
    #calculate entropy
    for x1 in attributeClass1:
        X1class=samplePool[columnList[-1]][samplePool[i]==x1]
        X1series=X1class.value_counts()
        attributeClassEntropy1=sum(math.log2(n/sum(X1series))*(-n/sum(X1series)) for n in X1series)
        attributeEntropy1 += attributeClassEntropy1*X1class.count()/len(samplePool)
    #save attribute and its entroy in a dictionary
    attributeDict[i]=attributeEntropy1
findIndex(attributeList)
attributeClass1=samplePool[splitList[1]].unique()
#remaining attribute could be used at current level
attributeList1 = removeAttribute(attributeList, 1)
for x1 in attributeClass1:
    treeDict2 = {}
    X1class=samplePool[columnList[-1]][samplePool[splitList[1]]==x1]
    X1series=X1class.value_counts()
    attributeClassEntropy1=sum(math.log2(n/sum(X1series))*(-n/sum(X1series)) for n in X1series) 
    attributeEntropy1 += attributeClassEntropy1*X1class.count()/len(samplePool)
    #get the mode value and its confidence of each class at the split attribute
    X1Mode = X1class.mode()[0]
    X1Confidence = str(X1series[X1Mode]/sum(X1series))
    #save the class and confidence in dictionary
    treeDict1[splitList[1]+': '+x1] = X1class.mode()[0]+' '+X1Confidence
    #Check if there are any remaining attributes to split
    if len(splitList) <= len(columnList):
        if attributeClassEntropy1 != 0:
            entropyCalculator(attributeList1, X1class)
            if len(splitList) < 3:
                findIndex(attributeList1)
            attributeClass2=samplePool[splitList[2]].unique()
            attributeList2 = removeAttribute(attributeList1, 2)
            for x2 in attributeClass2:
                treeDict3 = {}
                X2class=X1class[samplePool[splitList[2]]==x2]
                X2series=X2class.value_counts()
                attributeClassEntropy2=sum(math.log2(n/sum(X2series))*(-n/sum(X2series)) for n in X2series)
                X2Mode = X2class.mode()[0]
                X2Confidence = str(X2series[X2Mode]/sum(X2series))
                #get the mode value and its confidence of each class at the split attribute
                treeDict2[splitList[2]+': '+x2] = X2class.mode()[0]+' '+X2Confidence
                #Check if there are any remaining attributes to split
                if len(splitList) <= len(columnList):
                    if attributeClassEntropy2 != 0:
                        entropyCalculator(attributeList2, X2class)
                        if len(splitList) < 4:
                            findIndex(attributeList2)
                        attributeClass3=samplePool[splitList[3]].unique()
                        attributeList3 = removeAttribute(attributeList2, 3)
                        for x3 in attributeClass3:
                            treeDict4 = {}
                            X3class=X2class[samplePool[splitList[3]]==x3]
                            X3series=X3class.value_counts()
                            attributeClassEntropy3=sum(math.log2(n/sum(X3series))*(-n/sum(X3series)) for n in X3series)
                            X3Mode = X3class.mode()[0]
                            X3Confidence = str(X3series[X3Mode]/sum(X3series))
                            #get the mode value and its confidence of each class at the split attribute
                            treeDict3[splitList[3]+': '+x3] = X3class.mode()[0]+' '+X3Confidence
                            #Check if there are any remaining attributes to split
                            if len(splitList) <= len(columnList):
                                if attributeClassEntropy3 != 0:
                                    entropyCalculator(attributeList3, X3class)
                                    if len(splitList) < 5:
                                        findIndex(attributeList3)
                                    attributeClass4=samplePool[splitList[4]].unique()
                                    for x4 in attributeClass4:
                                        X4class=X3class[samplePool[splitList[4]]==x4]
                                        X4series=X4class.value_counts()
                                        attributeClassEntropy4=sum(math.log2(n/sum(X4series))*(-n/sum(X4series)) for n in X4series)
                                        X4Mode = X4class.mode()[0]
                                        X4Confidence = str(X4series[X4Mode]/sum(X4series))
                                        #get the mode value and its confidence of each class at the split attribute
                                        treeDict4[splitList[4]+': '+x4] = X4class.mode()[0]+' '+X4Confidence
                                    treeDict3[splitList[3]+': '+x3] = treeDict4
                        treeDict2[splitList[2]+': '+x2] = treeDict3
            treeDict1[splitList[1]+': '+x1] = treeDict2
#Show the tree structure
#Code from https://blog.csdn.net/u013061183/article/details/77231751
treeDict['Root:']=treeDict1
print(json.dumps(treeDict, indent=2))
#End of code from https://blog.csdn.net/u013061183/article/details/77231751

#Draw a tree structure graph
#Code from https://stackoverflow.com/questions/13688410/dictionary-object-to-decision-tree-in-pydot
def draw(parent_name, child_name):
    edge = pydot.Edge(parent_name, child_name)
    graph.add_edge(edge)

def visit(node, parent=None):
    for k,v in node.items():
        if isinstance(v, dict):
            # We start with the root node whose parent is None
            # we don't want to graph the None node
            if parent:
                draw(parent, parent+'\n'+k)
            if parent == None:
                visit(v, k)
            else:
                visit(v, parent+'\n'+k) 
        else:
            draw(parent, parent+'\n'+k)
            # drawing the label using a distinct name
            draw(parent+'\n'+k, parent+'\n'+k+'\n'+v)

graph = pydot.Dot(graph_type='graph')
visit(treeDict)
graph.write_png('treeDict_graph.png')
#End of code from https://stackoverflow.com/questions/13688410/dictionary-object-to-decision-tree-in-pydot