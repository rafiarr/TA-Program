import csv
import sys
import os
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
    for i in range(10):
        print alerts[i].sig_name

def testSVM():
    os = OsHandler('dataset/LLDOS-1','test')
    svmHandler = SVMHandler('dataset/LLDOS-1/datatrain.csv')
    data = os.csvReader(svmHandler.dataTrainPath)
    svmHandler.readDataTrain(data)
    fValue = testAlert()
    print svmHandler.predict(fValue)
    # print fValu
    return 0


def main():
    # testAlert()
    # testOsHandler()
    testSVM()

if __name__ == '__main__':
    main()

# Data :
# '1','2000-03-07 06:51:36','172.16.115.1','202.77.162.213','Ya','8','Tidak menggunakan TCP','Tidak menggunakan TCP','Tidak menggunakan UDP','Tidak menggunakan UDP','ICMP PING','misc-activity'
# '2','2000-03-07 06:51:36','202.77.162.213','172.16.115.1','Ya','0','Tidak menggunakan TCP','Tidak menggunakan TCP','Tidak menggunakan UDP','Tidak menggunakan UDP','ICMP Echo Reply','misc-activity'