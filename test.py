import csv
import sys
import os
import time
from alert import *
from oshandler import *
from classificationhandler import *

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

def testOsHandler():
    os = OsHandler('dataset/LLDOS-1','test')
    
    alerts = os.getAlertinDataset()
    
    alertList = []

    for i in range(len(alerts)):
        if( (alerts[i].sig_name in alertList) == False):
            alertList.append(alerts[i].sig_name)
    
    trainReader = os.dataTrainReader()

    svmHandler = SVMHandler(trainReader)

    acm = AlertCausalityMatrix(alertList)

    # count = 0
    path = os.outputFileDirPath + "correlated-value.txt"
    outputFile = open(path,"wb")
    
    output = "Hasil correlation"
    count = 0

    start_time = time.time()

    for i in range(len(alerts)):
        for j in range(len(alerts)):
            correlation = AlertCorrelation(alerts[i],alerts[j])
            alert1 = correlation.alert1.sig_name
            alert2 = correlation.alert2.sig_name
            

            
            correlationValues = correlation.getValues()
            
            # print correlationValues
            # print "prediction : " + str(svmHandler.predict(correlationValues))
            if(svmHandler.predict(correlationValues) == '1'):
                acm.incrementACMValue(alert1,alert2)
                output = alert1 + "," +alert2+" : "+str(correlationValues)+"\n"
                outputFile.write(output)
                count = count +1
            # else:
                
                # print alert1
                # print alert2

            # count = count+1
            # if(count == 5):
            #     break

        # if(count == 5):
        #     break
    outputFile.close()
    print count
    print "selesai alert correlation"
    print "--- "+str(time.time() - start_time) +" seconds ---"

    acm.calculateAllSigmaValue()
    for row in acm.causalityMatrix:
        print row

    acm.getRelatedList() 

# def testSVM():
#     os = OsHandler('dataset/LLDOS-1','test')
#     svmHandler = SVMHandler('dataset/LLDOS-1/datatrain.csv')
#     data = os.csvReader(svmHandler.dataTrainPath)
#     svmHandler.readDataTrain(data)
#     fValue = testAlert()
#     print svmHandler.predict(fValue)
#     # print fValu
#     return 0


def main():
    # testAlert()
    testOsHandler()
    # testSVM()

    # testValue = ["rafiar","nafiar","rina"]
    # train = "sekbay"
    # train2 = "rafiar"
    # print train2 in testValue

if __name__ == '__main__':
    main()

# Data :
# '1','2000-03-07 06:51:36','172.16.115.1','202.77.162.213','Ya','8','Tidak menggunakan TCP','Tidak menggunakan TCP','Tidak menggunakan UDP','Tidak menggunakan UDP','ICMP PING','misc-activity'
# '2','2000-03-07 06:51:36','202.77.162.213','172.16.115.1','Ya','0','Tidak menggunakan TCP','Tidak menggunakan TCP','Tidak menggunakan UDP','Tidak menggunakan UDP','ICMP Echo Reply','misc-activity'