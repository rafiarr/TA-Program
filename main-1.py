import csv
import sys
import os
import time
from alert import *

def ipToBinary(ipAddr):
    
    ip = ipAddr.split(".")
    
    fullBinary = ''
    for number in ip:
        binary = "{0:08b}".format(int(number))
        fullBinary += binary
        
    return fullBinary

def alertCsvReader(filepath,filename):
    f = open(filepath, 'rb')
    alerts = []
    reader = csv.reader(f)
    count = 1
    for row in reader:
        alert = Alert(row[1], #timestamp
                      row[2], #ip_dst
                      row[3], #ip_src
                      row[4], #icmp_status
                      row[5], #icmp_type
                      row[6], #tcp_dport
                      row[7], #tcp_sport
                      row[8], #udp_dport
                      row[9], #udp_sport
                      row[10], #sig_name
                      row[11], #sig_class_name
                      filename) #phase
        alerts.append(alert)
    f.close()
    return alerts    

def sigClassCsvReader(signatureClassFile):
    f = open(signatureClassFile,'rb')
    reader = csv.reader(f)
    sigClass = {}
    for row in reader:
        sigClass[row[1]] = row[0]

    f.close()
    return sigClass

def getAlertinDataset(dataset):
    alerts = []
    for dirname, dirnames, filenames in os.walk(dataset):
            
        for filename in filenames:
            filePath = os.path.join(dirname, filename)
            fileName = filename.split('.')[0]
            
            tempAlerts = []
            tempAlerts = alertCsvReader(filePath,fileName)
            for x in range(len(tempAlerts)):
                alerts.append(tempAlerts[x])

        if '.git' in dirnames:
            dirnames.remove('.git')
    
    newList = sorted(alerts, key=lambda alert: alert.timestamp)

    return newList

def main():

    dataset = 'dataset/LLDOS-1'
    #signatureClassFile = 'dataset/sig_class.csv'

    outputFileLocation = "output/main-1-"

    secondTimeFrame = 10

    #sigClass = sigClassCsvReader(signatureClassFile)

    timeSortedAlerts = getAlertinDataset(dataset)

    for i in range(len(timeSortedAlerts)):
        timeSortedAlerts[i].setId(i+1)

    timeFrameList = []

    firstAlertTimestamp  = timeSortedAlerts[0].timestamp
    lastAlertTimestamp   = timeSortedAlerts[-1].timestamp

    startTime   = time.mktime(time.strptime(firstAlertTimestamp, "%Y-%m-%d %H:%M:%S"))
    endTime     = time.mktime(time.strptime(lastAlertTimestamp, "%Y-%m-%d %H:%M:%S"))

    firstTime   = startTime
    lastTime    = startTime + (secondTimeFrame - 1)



    while True:
        
        newTimeFrame = TimeFrame(firstTime,lastTime)
        timeFrameList.append(newTimeFrame)

        # print newTimeFrame.alerts
        
        if(endTime < lastTime):
            
            break
        
        else:
            
            firstTime   = lastTime + 1
            lastTime    = firstTime + (secondTimeFrame - 1)  

    pointer = 0

    for i in range(len(timeSortedAlerts)):
        
        newListTime = time.mktime(time.strptime(timeSortedAlerts[i].timestamp, "%Y-%m-%d %H:%M:%S"))
    
        if (newListTime <= timeFrameList[pointer].endTime):
            
            timeFrameList[pointer].appendNewAlert(timeSortedAlerts[i])
            
        else:
            
            while (newListTime > timeFrameList[pointer].endTime) :
    
                pointer = pointer+1

            timeFrameList[pointer].appendNewAlert(timeSortedAlerts[i])
            
    for i in range(len(timeFrameList)):
        
        output = "Time Frame : " +str(i)+" Start Time :" +str(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(timeFrameList[i].startTime)))+ "\n"

        path = outputFileLocation + "alerts-" + str(i) + ".txt"
        
        outputFile =  open(path,"wb")
        
        outputFile.write(output)
        
        alertsInTimeFrame = timeFrameList[i].alerts 

        for j in range(len(alertsInTimeFrame)):
            
            output = "Alert Id : " +str(alertsInTimeFrame[j].alertId)+" Time : "+str(alertsInTimeFrame[j].timestamp)+ "\n"
            outputFile.write(output)
        
        outputFile.close()    
    
    for i in range(len(timeFrameList)):
        
        output = "Time Frame : " +str(i)+" Start Time :" +str(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(timeFrameList[i].startTime)))+ "\n"

        path = outputFileLocation + "correlation-" + str(i) + ".txt"
        
        outputFile =  open(path,"wb")
        
        outputFile.write(output)
        
        output = "Alert Id j,Alert Id i,F1,F2,F3,F4,F5"

        alertsInTimeFrame = timeFrameList[i].alerts 

        correlatedAlerts = []

        for j in range(len(alertsInTimeFrame)):
            for k in range(len(alertsInTimeFrame)):
                
                correlation = AlertCorrelation(alertsInTimeFrame[k],alertsInTimeFrame[j])
                
                f1 = correlation.calculateF1()
                f2 = correlation.calculateF2()
                f3 = correlation.calculateF3()
                f4 = correlation.calculateF4()
                f5 = (f1+f2+f3+f4)/4

                if (f5 >= 0.75):
                    correlatedAlerts.append(correlation)
            
                output = str(correlation.alert1.alertId)+","+str(correlation.alert2.alertId)+","+str(f1)+","+str(f2)+","+str(f3)+","+str(f4)+","+str(f5)+"\n"
                outputFile.write(output)
        
        output = "\n\n\nCorrelation with F5 value >= 0.75\n"
        outputFile.write(output)

        for j in range(len(correlatedAlerts)):
            alert1 = correlatedAlerts[j].alert1
            alert2 = correlatedAlerts[j].alert2
            if(alert1.alertId == alert2.alertId):
                continue
            output = "Id-1 : "+str(alert1.alertId)+", Sig Class : "+str(alert1.sig_class_name)+", Id-2 : "+str(alert2.alertId)+", Sig Class : "+str(alert2.sig_class_name)+"\n"
            outputFile.write(output)
        outputFile.close()



if __name__ == '__main__':
    main()



