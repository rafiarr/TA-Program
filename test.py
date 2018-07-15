import csv
import sys
import os
import time
from alert import *
from oshandler import *
from classificationhandler import *
from graphdrawer import *
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier

def testAlert():
    alert1 = Alert("2000-03-07 06:51:36","172.16.115.1","202.77.162.213","Ya","8","Tidak menggunakan TCP","Tidak menggunakan TCP","Tidak menggunakan UDP","Tidak menggunakan UDP","ICMP PING","misc-activity","test")
    alert2 = Alert("2000-03-07 06:51:36","202.77.162.213","172.16.115.1","Ya","0","Tidak menggunakan TCP","Tidak menggunakan TCP","Tidak menggunakan UDP","Tidak menggunakan UDP","ICMP Echo Reply","misc-activity","test")
    print 'Alert 1 Content :'
    print alert1.timestamp
    # print '\n\n'
    print 'Alert 2 Content :'
    print alert2.timestamp
    correlation = AlertCorrelation(alert1,alert2)
    fValue = []
    fValue.append(correlation.calculateF1())
    fValue.append(correlation.calculateF2())
    fValue.append(correlation.calculateF3())
    fValue.append(correlation.calculateF4())
    fValue.append(correlation.calculateF5())
    fValue.append(correlation.calculateF6())
    # print fValue
    # f6 = correlation.calculateF6()
    # print "F6 : "+str(f6)
    return fValue

# def testOsHandler():
#     # os = OsHandler('dataset/LLDOS-1','test')
    
#     alerts = os.getAlertinDataset()
    
#     alertList = []

#     for i in range(len(alerts)):
#         if( (alerts[i].sig_name in alertList) == False):
#             alertList.append(alerts[i].sig_name)
    
#     trainReader = os.dataTrainReader()

#     svmHandler = SVMHandler(trainReader)

#     acm = AlertCausalityMatrix(alertList)

#     # count = 0
#     path = os.outputFileDirPath + "correlated-value.txt"
#     outputFile = open(path,"wb")
    
#     output = "Hasil correlation"
#     count = 0

#     start_time = time.time()

#     for i in range(len(alerts)):
#         for j in range(len(alerts)):
#             correlation = AlertCorrelation(alerts[i],alerts[j])
#             alert1 = correlation.alert1.sig_name
#             alert2 = correlation.alert2.sig_name
             
#             correlationValues = correlation.getValues()
            
#             # print correlationValues
#             # print "prediction : " + str(svmHandler.predict(correlationValues))
#             if(svmHandler.predict(correlationValues) == '1'):
#                 acm.incrementACMValue(alert1,alert2)
#                 output = alert1 + "," +alert2+" : "+str(correlationValues)+"\n"
#                 outputFile.write(output)
#                 count = count +1
#             # else:
                
#                 # print alert1
#                 # print alert2

#             # count = count+1
#             # if(count == 5):
#             #     break

#         # if(count == 5):
#         #     break,.
#     outputFile.close()
#     print count
#     print "selesai alert correlation"
#     print "--- "+str(time.time() - start_time) +" seconds ---"

#     acm.calculateAllSigmaValue()
#     for row in acm.causalityMatrix:
#         print row

#     relatedList = acm.getRelatedList() 
#     edgeList = []
#     labelList = []
#     for row in relatedList:
#         edgeList.append(row.keys()[0])
#         labelList.append(row.values()[0])
    
#     graphDrawer = GraphDrawer(edgeList,labelList)
#     print graphDrawer.graph 
#     print graphDrawer.labels

#     graphDrawer.draw_graph()
# # def testSVM():
# #     os = OsHandler('dataset/LLDOS-1','test')
# #     svmHandler = SVMHandler('dataset/LLDOS-1/datatrain.csv')
# #     data = os.csvReader(svmHandler.dataTrainPath)
# #     svmHandler.readDataTrain(data)
# #     fValue = testAlert()
# #     print svmHandler.predict(fValue)
# #     # print fValu
# #     return 0


# def testNewDataset():
#     # os = OsHandler('dataset/LLDOS-1.0/alert','test')
#     alerts = os.getAlertinDataset2('dataset/LLDOS-1.0/alert')
    
#     alertList = []

#     for i in range(len(alerts)):
#         if( (alerts[i].sig_name in alertList) == False):
#             alertList.append(alerts[i].sig_name)
#             print alerts[i].sig_name
    


def testtime():
    # strftime("%a, %d %b %Y %H:%M:%S", gmtime())
    currentTime = time.strftime("%a,%d%b%Y-%H:%M:%S", time.gmtime())
    outputPath = 'output/' + currentTime + '/'
    if not os.path.exists(outputPath):
        os.mkdir(outputPath)
        if os.path.exists(outputPath):
            print 'done'

    outputArray = []
    outputRow = []
    outputRow.append("coba output")
    outputRow.append("\n")
    outputArray.append(outputRow)
    outputRow = []
    outputRow.append("coba output, ")
    outputRow.append("coba output, ")
    outputRow.append("coba output")
    outputRow.append("\n")
    outputArray.append(outputRow)

    outputFile = outputPath + 'tes.txt'

    osHandler = OSHandler()
    osHandler.printArray(outputFile,outputArray)

    # trainReader = os.dataTrainReader()
def testArray():
    array = []
    for i in range(1597):
        for j in range(1597):
            column = [1,1,1,1,1,1]
            array.append(column)
    print "berhasil"

def testMLP():

    currentTime = time.strftime("%a,%d%b%Y-%H:%M:%S", time.gmtime())
    
    # Buat folder + file output, file output alert, file output fitur, file output acm, file output graf path
    outputPath      = 'output/' + currentTime+'/'
    fileOutputAlert = outputPath + 'alert.txt'
    fileFiturAlert  = outputPath + 'fitur.txt'
    fileTabelAcm    = outputPath + 'acm.txt'
    fileGraf        = outputPath + 'graf.txt'

    # Inisiasi osHandler, buat folder
    osHandler = OSHandler()
    osHandler.createDirectory(outputPath)
    trainReader = osHandler.dataTrainReader('dataset/DataTrain/datatrain2.csv')
    reader = trainReader
    xList = []
    yListSVM = []
    yListMLP = []
    for row in reader:

        tempList = []
        tempList.append(float(row[0]))
        tempList.append(float(row[1]))
        tempList.append(float(row[2]))
        tempList.append(float(row[3]))
        tempList.append(float(row[4]))
        tempList.append(float(row[5]))
        yListSVM.append(row[6])
        yListMLP.append(float(row[7]))
        xList.append(tempList)

    output = "Data train : "
    print output

    X = np.array(xList)
    y = np.array(yListMLP) 
    ySVM = yListSVM
    yMLP = yListMLP
    
    for i in range(len(X)):
        print str(X[i]) + ", " + str(ySVM[i])+ ", " + str(yMLP[i])
    print xList
    print X
    clfSVM = svm.SVC(probability=True,class_weight={'1':13,'-1':5},random_state=5)
    clfSVM.fit(X,ySVM)

    clfMLP = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(6,1),random_state=1)
    clfMLP.fit(X,yMLP)
    # scaler = StandardScaler()

def main():
    # testAlert()
    # testOsHandler()
    # testtime()
    testMLP()
    # testNewDataset()
    # testSVM()
    # testArray()
    # testValue = ["rafiar","nafiar","rina"]
    # train = "sekbay"
    # train2 = "rafiar"
    # print train2 in testValue

if __name__ == '__main__':
    main()

# Data :
# '1','2000-03-07 06:51:36','172.16.115.1','202.77.162.213','Ya','8','Tidak menggunakan TCP','Tidak menggunakan TCP','Tidak menggunakan UDP','Tidak menggunakan UDP','ICMP PING','misc-activity'
# '2','2000-03-07 06:51:36','202.77.162.213','172.16.115.1','Ya','0','Tidak menggunakan TCP','Tidak menggunakan TCP','Tidak menggunakan UDP','Tidak menggunakan UDP','ICMP Echo Reply','misc-activity'