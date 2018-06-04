import csv
import sys
import os
from alert import *

class OsHandler:
    datasetDirPath      = ''
    outputFileLocation  = ''
    def __init__(self,datasetPath,programName):
        self.datasetDirPath = datasetPath
        self.outputFileLocation = 'output/' + str(programName)

    def csvReader(self,filepath):
        filecsv = open(filepath, 'rb')
        reader = csv.reader(filecsv)
        filecsv.close
        return reader

    def alertCsvReader(self,filepath,filename):
        alerts = []
        reader = self.csvReader(filepath)
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
        return alerts

    # def dataTrainReader(self,):
    #     path = self.datasetDirPath + "/datatrain.csv"
    #     # print path dataset/LLDOS-1/datatrain.csvd
    #     reader = self.csvReader(path)
       
    #     npArray = []
    #     yList   = []
    #     for row in reader:
    #         xList = []
    #         xList.append(row[0])
    #         xList.append(row[1])
    #         xList.append(row[2])
    #         xList.append(row[3])
    #         xList.append(row[4])
    #         xList.append(row[5])
    #         yList.append(row[6])
    #         npArray.append(xList)
        
    #     # print npArray
    #     # print yList
    #     for i in range(len(yList)):
    #         print npArray[i]
    #         print yList[i]
    #     return 0
    #     # self

    def getAlertinDataset(self):
        alerts = []
        for dirname, dirnames, filenames in os.walk(self.datasetDirPath):
                
            for filename in filenames:
                filePath = os.path.join(dirname, filename)
                fileName = filename.split('.')[0]
                
                tempAlerts = []
                tempAlerts = self.alertCsvReader(filePath,fileName)
                for x in range(len(tempAlerts)):
                    alerts.append(tempAlerts[x])

            if '.git' in dirnames:
                dirnames.remove('.git')
        
        timeSortedAlerts = sorted(alerts, key=lambda alert: alert.timestamp)

        path = self.outputFileLocation + "-alerts.txt"
            
        outputFile =  open(path,"wb")

        output = "Id,timestamp,ip_dst,ip_src,icmp_status,icmp_type,tcp_dport,tcp_sport,udp_dport,udp_sport,sig_name,sig_class_name,phase"

        for i in range(len(timeSortedAlerts)):
            timeSortedAlerts[i].setId(i+1)
            output = str(timeSortedAlerts[i].alertId)+","+str(timeSortedAlerts[i].timestamp)+","+str(timeSortedAlerts[i].ip_dst)+","+str(timeSortedAlerts[i].ip_src)+","+str(timeSortedAlerts[i].icmp_status)+","+str(timeSortedAlerts[i].icmp_type)+","+str(timeSortedAlerts[i].tcp_dport)+","+str(timeSortedAlerts[i].tcp_sport)+","+str(timeSortedAlerts[i].udp_dport)+","+str(timeSortedAlerts[i].udp_sport)+","+str(timeSortedAlerts[i].sig_name)+","+str(timeSortedAlerts[i].sig_class_name)+","+str(timeSortedAlerts[i].phase)+"\n"
            outputFile.write(output)

        outputFile.close()

        return timeSortedAlerts