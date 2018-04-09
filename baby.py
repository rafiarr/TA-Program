import csv
import sys
import os
from alert import *

dataset = 'dataset/LLDOS-1'

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

def main():
    
    alerts = []
    for dirname, dirnames, filenames in os.walk('dataset/LLDOS-1'):
            
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
    count = 0
    for x in range(len(newList)):
        count = count+1
    print count

    print newList[0].ip_src

    print newList[1].ip_src

    correlation = AlertCorrelation(newList[0],newList[1])
    
    print correlation.calculateF1()

if __name__ == '__main__':
    main()



