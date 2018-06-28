import csv
import sys
import os
from alert import *

class OsHandler:
    
    datasetDirPath      = ''
    alertDirPath        = ''
    outputFileDirPath   = ''
    dataTrainDirPath    = ''
    programName         = ''

    def __init__(self,datasetPath,program):
        self.datasetDirPath     = datasetPath
        self.programName        = program
        self.alertDirPath       = self.datasetDirPath + '/alert'
        self.outputFileDirPath  = self.datasetDirPath + '/output/' + self.programName + '/'
        if not os.path.exists(self.outputFileDirPath):
            os.makedirs(self.outputFileDirPath)
        self.dataTrainDirPath   = self.datasetDirPath + '/train'


    def csvReader(self,filepath):
        filecsv = open(filepath, 'rb')
        reader = csv.reader(filecsv)
        filecsv.close
        return reader

    def alertCsvReader(self,filepath,filename):
        alerts = []
        reader = self.csvReader(filepath)
        # print reader
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

    def alert2CsvReader(self,filepath):
        alerts = []
        reader = self.csvReader(filepath)
        for row in reader:
            alert = Alert2(row[0],
                        row[1],
                        row[2],
                        row[3],
                        row[4],
                        row[5])
            alerts.append(alert)
        return alerts

    def dataTrainReader(self):

        path    = self.dataTrainDirPath + '/datatrain.csv'
        reader  = self.csvReader(path)
        output  = "\nInput data train dari "+path
        print output
        return reader

    def getAlertinDataset(self):

        output = "Input dataset alert di "+ self.alertDirPath
        print output + "\n"

        alerts = []
        for dirname, dirnames, filenames in os.walk(self.alertDirPath):
                
            for filename in filenames:
                filePath = os.path.join(dirname, filename)
                fileName = filename.split('.')[0]
                
                output = "input "+filename
                print output

                tempAlerts = []
                tempAlerts = self.alertCsvReader(filePath,fileName)
                for x in range(len(tempAlerts)):
                    alerts.append(tempAlerts[x])

            if '.git' in dirnames:
                dirnames.remove('.git')
        
        timeSortedAlerts = sorted(alerts, key=lambda alert: alert.timestamp)

        for i in range(len(timeSortedAlerts)):
            timeSortedAlerts[i].setId(i+1)

        path = self.outputFileDirPath + 'alerts.txt'
        # print self.outputFileDirPath
        outputFile =  open(path,"wb")

        output = "Id,timestamp,ip_dst,ip_src,icmp_status,icmp_type,tcp_dport,tcp_sport,udp_dport,udp_sport,sig_name,sig_class_name,phase"

        for i in range(len(timeSortedAlerts)):
            timeSortedAlerts[i].setId(i+1)
            output = str(timeSortedAlerts[i].alertId)+","+str(timeSortedAlerts[i].timestamp)+","+str(timeSortedAlerts[i].ip_dst)+","+str(timeSortedAlerts[i].ip_src)+","+str(timeSortedAlerts[i].icmp_status)+","+str(timeSortedAlerts[i].icmp_type)+","+str(timeSortedAlerts[i].tcp_dport)+","+str(timeSortedAlerts[i].tcp_sport)+","+str(timeSortedAlerts[i].udp_dport)+","+str(timeSortedAlerts[i].udp_sport)+","+str(timeSortedAlerts[i].sig_name)+","+str(timeSortedAlerts[i].sig_class_name)+","+str(timeSortedAlerts[i].phase)+"\n"
            outputFile.write(output)

        print "\nBerhasil input alert"
        output = "Jumlah alert yang di baca : " + str(len(timeSortedAlerts))
        print output
        output = "Data alert yang diinputkan tersimpan di " + path
        print output

        outputFile.close()

        return timeSortedAlerts

    def getAlertinDataset2(self,datasetPath):

        timeSortedAlerts = []

        alerts = []
        for dirname, dirnames, filenames in os.walk(datasetPath):
                
            for filename in filenames:
                filePath = os.path.join(dirname, filename)
                
                tempAlerts = self.alert2CsvReader(filePath)
                for alert in tempAlerts:
                    alerts.append(alert)

            if '.git' in dirnames:
                dirnames.remove('.git')

        timeSortedAlerts = sorted(alerts, key=lambda alert: alert.timestamp)
        
        for i in range(len(timeSortedAlerts)):
            timeSortedAlerts[i].setId(i+1)

        # for alert in timeSortedAlerts:
        #     alert.printAll()

        return timeSortedAlerts

def testData():
    os = OsHandler('dataset/LLDOS-1.0','test')
    os.getAlertinDataset2('dataset/LLDOS-1.0/alert')

if __name__ == '__main__' :
    testData()