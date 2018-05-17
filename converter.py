from __future__ import division
import csv
import time

def ipToBinary(ipAddr):
    
    ip = ipAddr.split(".")
    print ip
    fullBinary = ''
    for number in ip:
        binary = "{0:08b}".format(int(number))
        print binary
        fullBinary += binary
    print fullBinary    
    return fullBinary

def compareUrutan(string1,string2):
    
    count = 0
    for x in range(len(string1)):
        # printString = "index : " + str(x) + " string 1 : " + string1[x] + " string 2 : " + string2[x] 
        # print printString   
        if(string1[x] == string2[x]):
            count = count + 1

    return count

def compareIP(ipAddr1,ipAddr2):
    ipBin1 = ipToBinary(ipAddr1)
    # print ipToBinary(ipAddr1)
    ipBin2 = ipToBinary(ipAddr2)
    # print ipToBinary(ipAddr2)
    # print compareUrutan(ipBin1,ipBin2)
    return compareUrutan(ipBin1,ipBin2)


signatureClassFile = 'dataset/sig_class.csv'
f = open(signatureClassFile,'rb')
reader = csv.reader(f)
sigClass = {}
for row in reader:
    sigClass[row[1]] = row[0]

# print len(sigClass)

# print time.localtime(952386696.0)
# print time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(952386696.0))
firstList = [1,2,3,4]

newList = []

newList.append(firstList[2])

print newList

