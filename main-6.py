import csv
import sys
import os
import time
from decimal import *
from alert import *
from oshandler import *
from classificationhandler import *
from graphdrawer import *

def calculateCorrelationProbability(alerti,alertj,classificationHandler,acm):
    correlation = FeatureExtractor(alerti,alertj)
    alert1 = correlation.alert1.sig_name
    alert2 = correlation.alert2.sig_name

    if (acm.getACMValue(alert1,alert2) != 0):
        correlation.setF5(float(acm.calculateBackwardCorrelationStrength(alert1,alert2)))
        
    else:
        correlation.setF5(correlation.calculateF5())

    correlationValues = correlation.getValues()

    probaValue = classificationHandler.predictProba(correlationValues)
    classValue = classificationHandler.predict(correlationValues)
    
    return probaValue[0][0]

def main():
    
    # Dapetin waktu saat ini
    currentTime = time.strftime("%a,%d%b%Y-%H:%M:%S", time.gmtime())
    
    # Buat folder + file output, file output alert, file output fitur, file output acm, file output graf path
    outputPath      = 'output/' + currentTime+'LLDOS-1.0/'
    fileOutputAlert = outputPath + 'alert.txt'
    # fileFiturAlert  = outputPath + 'fitur.txt'
    fileTabelAcm    = outputPath + 'acm.txt'
    fileGraf        = outputPath + 'graf.txt'
    fileWaktuJalan  = outputPath + 'waktu.txt'
    outputWaktuArray = []
    # Inisiasi osHandler, buat folder
    osHandler = OSHandler()
    osHandler.createDirectory(outputPath)

    # Baca file alert, simpen di variable alerts
    outputRow = []
    outputRow.append("Waktu membaca dataset :")
    startTime = time.time()
    alerts, alertLists, alertFilenames = osHandler.getAlertinDataset3('dataset/LLDOS-1.0/')
    outputRow.append(" "+str(time.time() - startTime)+" detik")
    outputRow.append("\n")
    outputWaktuArray.append(outputRow)
    print len(alerts)
    # Dapetin jenis alert yang ada di dataset
    # Siapin yang mau di print ke file
    outputArray = []
    outputRow = []
    outputRow.append("Alert yang terdapat pada dataset")
    outputRow.append("\n")
    outputArray.append(outputRow)
    
    # Mulai ngecek alert apa aja yang ada
    for i in range(len(alertFilenames)):
        outputRow = []
        outputRow.append(alertFilenames[i])
        outputRow.append("\n")
        outputArray.append(outputRow)
        alertType = alertLists[i].getAlertTypeList()
        for j in range(len(alertType)) :
            outputRow = []
            outputRow.append(alertType[j])
            outputRow.append("\n")
            outputArray.append(outputRow)

    
    # outputArray = []
    outputRow = []
    outputRow.append("keseluruhan alert :")
    outputRow.append("\n")
    outputArray.append(outputRow)
    alertList = []
    count = 0
    for i in range(len(alerts)):
        if( (alerts[i].sig_name in alertList) == False):
            alertList.append(alerts[i].sig_name)
            count = count+1
            outputRow = []
            outputRow.append(str(i+1)+","+str(alerts[i].sig_name)) 
            outputRow.append("\n")
            outputArray.append(outputRow)       

    osHandler.printArray(fileOutputAlert,outputArray)

    # Inisiasi class classificationHandler buat model klasifikasi SVM
    trainReader = osHandler.dataTrainReader('dataset/DataTrain/datatrain.csv')
    classificationHandler = SVMHandler(trainReader)
    
    # Inisiasi tabel ACM
    acm = AlertCausalityMatrix(alertList)
 
    output = "Hasil correlation"
    count = 0

    correlationTreshold = 0.5
    # correlationSensitifity = 0.1

    edgeList = []

    hyperAlert = HyperAlert()

    # i = 10

    # print range(i)
    outputRow = []
    outputRow.append("waktu yang dibutuhkan untuk pembuatan hyper alert :")
    startTime = time.time()
    for j in range(len(alerts)):
        for i in range(j):
            if j == i:
                continue
            else:
                correlationProbability = calculateCorrelationProbability(alerts[i],alerts[j],classificationHandler,acm)
                

                if correlationProbability > correlationTreshold:
                    # print output
                    acm.incrementACMProbaValue(alerts[i].sig_name,alerts[j].sig_name,correlationProbability)    
                    hyperAlert.insertEgdeList(alerts[i].alertId,alerts[j].alertId,round(correlationProbability,2))

                    # if alerts[i].sig_name == 'BAD-TRAFFIC loopback traffic' or alerts[j].sig_name == 'BAD-TRAFFIC loopback traffic':
                    #     output = str(alerts[i].sig_name)+','+str(alerts[i].ip_src)+','+str(alerts[i].port_src)+','+str(alerts[i].ip_dst)+','+str(alerts[i].port_dst)+','+str(alerts[j].sig_name)+','+str(alerts[j].ip_src)+','+str(alerts[j].port_src)+','+str(alerts[j].ip_dst)+','+str(alerts[j].port_dst)
                    #     print output
    
    outputRow.append(" "+str(time.time() - startTime)+" detik")
    outputRow.append("\n")
    outputWaktuArray.append(outputRow)

    outputRow = []
    outputRow.append("Waktu yang dibutuhkan untuk membangun graf penyerangan :")
    startTime = time.time()
    correlationStrengthTreshold = 0.1
    hyperAlertEdge = hyperAlert.getEdgeList()
    visitedEdge = []

    for i in range(len(hyperAlertEdge)):
        # print hyperAlertEdge[i]
        alert1 = alerts[(hyperAlertEdge[i][0]-1)].sig_name
        alert2 = alerts[(hyperAlertEdge[i][1]-1)].sig_name
        if len(visitedEdge) == 0:
            
            forwardCorrelationStrength = acm.calculateForwardCorrelationStrength(alert1,alert2)
            # output = str(alert1)+', '+str(alert2)+', '+str(round(forwardCorrelationStrength,2))
            # print output
            if(forwardCorrelationStrength > correlationStrengthTreshold):
                newEdge = (alert1,alert2,round(forwardCorrelationStrength,2))
                visitedEdge.append(newEdge)
        else:
            visited = 0
            for i in range(len(visitedEdge)):
                if alert1 == visitedEdge[i][0] and alert2 == visitedEdge[i][1]:
                    visited = 1
            if visited:
                continue
            else:
                forwardCorrelationStrength = acm.calculateForwardCorrelationStrength(alert1,alert2)
                # output = str(alert1)+', '+str(alert2)+', '+str(round(forwardCorrelationStrength,2))
                # print output
                if(forwardCorrelationStrength > correlationStrengthTreshold):
                    newEdge = (alert1,alert2,round(forwardCorrelationStrength,2))
                    visitedEdge.append(newEdge)
                else:
                    continue
    outputRow.append(" "+str(time.time() - startTime)+" detik")
    outputRow.append("\n")
    outputWaktuArray.append(outputRow)

    outputArray = []
    outputRow = []
    outputRow.append("acm value")
    outputRow.append("\n")
    outputArray.append(outputRow)
    for i in range(len(alertList)):
        output = ''
        for j in range(len(alertList)):
            output = output + str(acm.getACMValue(alertList[i],alertList[j]))+',' 
        outputRow = []
        outputRow.append(output)
        outputRow.append("\n")
        outputArray.append(outputRow)

    outputRow = []
    outputRow.append("forward correlation strength")
    outputRow.append("\n")
    outputArray.append(outputRow)
    # acmMatrix = acm.causalityMatrix
    print alertList
    for i in range(len(alertList)):
        output = ''
        for j in range(len(alertList)):
            output = output + str(acm.calculateForwardCorrelationStrength(alertList[i],alertList[j]))+','
        outputRow = []
        outputRow.append(output)
        outputRow.append("\n")
        outputArray.append(outputRow)

    attackGraphEdge = []
    correlationStrengthTreshold = 0.1
    for i in range(len(alertList)):
        for j in range(len(alertList)):
            forwardCorrelationStrength = acm.calculateForwardCorrelationStrength(alertList[i],alertList[j])
            if(forwardCorrelationStrength > correlationStrengthTreshold):
                newEdge = {(alertList[i],alertList[j]):round(forwardCorrelationStrength,2)}
                attackGraphEdge.append(newEdge)
    
    osHandler.printArray(fileTabelAcm,outputArray)

    attackGraphEdge = []
    outputArray = []
    outputRow = []
    outputRow.append("attack graph")
    outputRow.append("\n")
    outputArray.append(outputRow)
    for row in visitedEdge:
        outputRow = []
        newEdge = {(row[0],row[1]):row[2]}
        outputRow.append("{("+str(row[0])+","+str(row[1])+"):"+str(row[2])+"}")
        outputRow.append("\n")
        outputArray.append(outputRow)
        attackGraphEdge.append(newEdge)

    osHandler.printArray(fileGraf,outputArray)
    osHandler.printArray(fileWaktuJalan,outputWaktuArray)
    
    edgeList = []
    labelList = []
    for row in attackGraphEdge:
        edgeList.append(row.keys()[0])
        labelList.append(row.values()[0])

    graphDrawer = GraphDrawer(edgeList,labelList)

    graphDrawer.draw_graph()
    


    
if __name__ == '__main__':
    main()



