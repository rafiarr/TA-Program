import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib import style
# style.use("ggplot")
from sklearn import svm

class SVMHandler:
    X               = []
    y               = []
    clf             = []
    dataTrainPath   = ''
    def __init__(self,dataTrain):
        self.dataTrainPath = dataTrain
    
    def predict(self,newList):
        xList = []
        xList.append(newList)
        # xList = np.array(xList)
        y = self.clf.predict(xList)
        return y

    def readDataTrain(self,reader):
        
        xList = []
        yList = []

        for row in reader:
            newList = []
            newList.append(row[0])
            newList.append(row[1])
            newList.append(row[2])
            newList.append(row[3])
            newList.append(row[4])
            newList.append(row[5])
            yList.append(row[6])
            xList.append(newList)
        # print xList
        # print yList
        self.X = np.array(xList)
        print self.X
        self.y = yList
        self.clf = svm.SVC()
        self.clf.fit(self.X,self.y)
        
        return 0

    