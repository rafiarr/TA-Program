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
    fValue = []
    for i in range(len(newList)):
        for j in range(len(newList)):
            correlation = AlertCorrelation(newList[j] # current alert
                                            ,newList[i]) #previous alert
            f1 = correlation.calculateF1()
            f2 = correlation.calculateF2()
            f3 = correlation.calculateF3()
            f4 = correlation.calculateF4()
            print "cid1 : " +str(j+1)+", cid2 : " +str(i+1)+", F1 : " +str(f1)+ ", F2 : "+str(f2)+", F3 : "+str(f3)+", F4 : "+str(f4)
if __name__ == '__main__':
    main()



