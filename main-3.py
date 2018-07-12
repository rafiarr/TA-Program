import csv
import sys
import os
import time
from alert import *
from oshandler import *
from classificationhandler import *
from graphdrawer import *

def main():
    
    # Dapetin waktu saat ini
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

    # Baca file alert, simpen di variable alerts
    alerts = osHandler.getAlertinDataset('dataset/lldos2/')
    
    # Dapetin jenis alert yang ada di dataset
    # Siapin yang mau di print ke file
    outputArray = []
    outputRow = []
    outputRow.append("Alert yang terdapat pada dataset")
    outputRow.append("\n")
    outputArray.append(outputRow)
    
    # Mulai ngecek alert apa aja yang ada
    alertList = []
    count = 0
    for i in range(len(alerts)):
        if( (alerts[i].sig_name in alertList) == False):
            alertList.append(alerts[i].sig_name)
            count = count+1
            output = str(count)+' '+alerts[i].sig_name
            outputRow = []
            outputRow.append(output)
            outputRow.append("\n")
            outputArray.append(outputRow)
    
    osHandler.printArray(fileOutputAlert,outputArray)
    outputArray = []

    # Inisiasi class SVMHandler buat model klasifikasi SVM
    trainReader = osHandler.dataTrainReader('dataset/DataTrain/')
    svmHandler = SVMHandler(trainReader)
    
    # Inisiasi tabel ACM
    acm = AlertCausalityMatrix(alertList)
 
    output = "Hasil correlation"
    count = 0

    start_time = time.time()

    for i in range(len(alerts)):
        for j in range(len(alerts)):
            correlation = AlertCorrelation(alerts[i],alerts[j])
            alert1 = correlation.alert1.sig_name
            alert2 = correlation.alert2.sig_name
             
            correlationValues = correlation.getValues()
            
            probaValue = svmHandler.predictProba(correlationValues)
            classValue = svmHandler.predict(correlationValues)
            print str(probaValue[0][0])+', '+str(classValue)
            acm.incrementACMProbaValue(alert1,alert2,probaValue[0][0])
            # print correlationValues
            # print "prediction : " + str(svmHandler.predict(correlationValues))
            # if(svmHandler.predict(correlationValues) == '1'):
            #     acm.incrementACMValue(alert1,alert2)
            #     # output = alert1 + "," +alert2+" : "+str(correlationValues)+"\n"
            #     # outputFile.write(output)
            #     count = count +1
            # else:
                
                # print alert1
                # print alert2

            # count = count+1
            # if(count == 5):
            #     break

        # if(count == 5):
        #     break,.
    # outputFile.cl  osHandlere()
    print count
    print "selesai alert correlation"
    print "--- "+str(time.time() - start_time) +" seconds ---"

    acm.calculateAllSigmaValue()
    for row in acm.causalityMatrix:
        print row

    relatedList = acm.getRelatedList() 
    edgeList = []
    labelList = []
    for row in relatedList:
        edgeList.append(row.keys()[0])
        labelList.append(row.values()[0])
    
    graphDrawer = GraphDrawer(edgeList,labelList)
    print graphDrawer.graph 
    print graphDrawer.labels

    graphDrawer.draw_graph()
    
if __name__ == '__main__':
    main()



