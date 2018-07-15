import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib import style
# style.use("ggplot")
from sklearn import svm
from sklearn.neural_network import MLPClassifier


class SVMHandler:
    X               = []
    y               = []
    clf             = []
    dataTrainPath   = ''
    def __init__(self,reader):
       
        xList = []
        yList = []

        for row in reader:

            tempList = []
            tempList.append(row[0])
            tempList.append(row[1])
            tempList.append(row[2])
            tempList.append(row[3])
            tempList.append(row[4])
            tempList.append(row[5])
            yList.append(row[6])
            xList.append(tempList)

        output = "Data train : "
        print output

        self.X = np.array(xList) 
        self.y = yList
        for i in range(len(self.X)):
            print str(self.X[i]) + ", " + str(self.y[i])
        self.clf = svm.SVC(probability=True,class_weight={'1':13,'-1':5},random_state=5)
        self.clf.fit(self.X,self.y)
    
    def predict(self,tempList):
        xList = []
        xList.append(tempList)
        # xList = np.array(xList)
        y = self.clf.predict(xList)
        # print y
        return y

    def predictProba(self,tempList):
        xList = []
        xList.append(tempList)
        # xList = np.array(xList)
        y = self.clf.predict_proba(xList)
        # print y
        return y

    # def readDataTrain(self,reader):
        
    #     xList = []
    #     yList = []

    #     for row in reader:
    #         tempList = []
    #         tempList.append(row[0])
    #         tempList.append(row[1])
    #         tempList.append(row[2])
    #         tempList.append(row[3])
    #         tempList.append(row[4])
    #         tempList.append(row[5])
    #         yList.append(row[6])
    #         xList.append(tempList)

    #     self.X = np.array(xList)
    #     print self.X
    #     self.y = yList
    #     self.clf = svm.SVC()
    #     self.clf.fit(self.X,self.y)
        
    #     return 0

class ClassificationHandler:
    X               = []
    ySVM            = []
    yMLP            = []
    clfSVM          = []
    clfMLP          = []
    dataTrainPath   = ''
    def __init__(self,reader):
       
        xList = []
        yListSVM = []
        yListMLP = []
        for row in reader:

            tempList = []
            tempList.append(row[0])
            tempList.append(row[1])
            tempList.append(row[2])
            tempList.append(row[3])
            tempList.append(row[4])
            tempList.append(row[5])
            yListSVM.append(row[6])
            yListMLP.append(row[7])
            xList.append(tempList)

        output = "Data train : "
        print output

        self.X = np.array(xList) 
        self.ySVM = yListSVM
        self.yMLP = yListMLP
        
        for i in range(len(self.X)):
            print str(self.X[i]) + ", " + str(self.ySVM[i])+ ", " + str(self.yMLP[i])
        
        self.clfSVM = svm.SVC(probability=True,class_weight={'1':13,'-1':5},random_state=5)
        self.clfSVM.fit(self.X,self.ySVM)
    
        self.clfMLP = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(6,1),random_state=1)
        self.clfMLP.fit(self.X,self.yMLP)

    def predict(self,tempList):
        xList = []
        xList.append(tempList)
        # xList = np.array(xList)
        y = self.clfSVM.predict(xList)
        # print y
        return y

    def predictProba(self,tempList):
        xList = []
        xList.append(tempList)
        # xList = np.array(xList)
        ySVM = self.clfSVM.predict_proba(xList)
        yMLP = self.clfMLP.predict_proba(xList) 
        if ySVM > yMLP:
            return ySVM
        else:
            return yMLP
        # print y