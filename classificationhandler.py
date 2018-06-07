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
        self.clf = svm.SVC(probability=True,class_weight={'1':13,'-1':5})
        self.clf.fit(self.X,self.y)
    
    def predict(self,tempList):
        xList = []
        xList.append(tempList)
        # xList = np.array(xList)
        y = self.clf.predict(xList)
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

    