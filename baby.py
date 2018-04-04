import csv
import sys
import os

dataset = 'dataset/LLDOS-1'

def alertCsvReader(filepath,filename):
    f = open(filepath, 'rb')
    alerts = []
    reader = csv.reader(f)
    for row in reader:
        alert = {'timestamp': row[1],
                'ip_dst': row[2],
                'ip_dst': row[3],
                'icmp':row[4],
                'icmp_type':row[5],
                'tcp_dport':row[6],
                'tcp_sport':row[7],
                'udp_dport':row[8],
                'udp_sport':row[9],
                'sig_name':row[10],
                'sig_class_name':row[11],
                'phase':filename}
        alerts.append(alert)
    f.close()
    return alerts    

def main():
    
    # for x in range(len(alerts)):
    #     print alerts[x]
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
    
    fileName = ''
    for x in range(len(alerts)):
        if alerts[x]['phase'] != fileName:
            fileName = alerts[x]['phase']
            print fileName
        else:
            continue

if __name__ == '__main__':
    main()



