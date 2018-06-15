from __future__ import division
import time

class Alert:
    alertId         = 0
    timestamp       = ''
    ip_dst          = ''
    ip_src          = ''
    icmp_status     = ''
    icmp_type       = ''
    tcp_dport       = ''
    tcp_sport       = ''
    udp_dport       = ''
    udp_sport       = ''
    sig_name        = ''
    sig_class_name  = ''
    phase           = ''
    def __init__(self,
                file_timestamp,
                file_ip_dst,
                file_ip_src,
                file_icmp_status,
                file_icmp_type,
                file_tcp_dport,
                file_tcp_sport,
                file_udp_dport,
                file_udp_sport,
                file_sig_name,
                file_sig_class_name,
                file_phase):
        self.timestamp      = file_timestamp
        self.ip_dst         = file_ip_dst
        self.ip_src         = file_ip_src
        self.icmp_status    = file_icmp_status
        self.icmp_type      = file_icmp_type
        self.tcp_dport      = file_tcp_dport
        self.tcp_sport      = file_tcp_sport
        self.udp_dport      = file_udp_dport
        self.udp_sport      = file_udp_sport
        self.sig_name       = file_sig_name
        self.sig_class_name = file_sig_class_name
        self.phase          = file_phase

    def setId(self,newId):
        self.alertId = newId

class AlertCorrelation:
    alert1      = []
    alert2      = []
    f1          = 0
    f2          = 0
    f3          = 0
    f4          = 0
    f5          = 0
    f6          = 0
    tracehold   = 0.5
    def __init__(self,alert1,alert2):
        self.alert1 = alert1
        self.alert2 = alert2
        self.f1     = self.calculateF1()
        self.f2     = self.calculateF2()
        self.f3     = self.calculateF3()
        self.f4     = self.calculateF4()
        self.f5     = self.calculateF5()
        self.f6     = self.calculateF6()
        
        
        # if (self.f1 >= self.tracehold and self.f2 >= self.tracehold)


    def ipToBinary(self,ipAddr):
        
        ip = ipAddr.split(".")
        fullBinary = ''
        for number in ip:
            binary = "{0:08b}".format(int(number))
            fullBinary += binary    
        return fullBinary
    
    def compareUrutan(self,string1,string2):
        
        count = 0
        for x in range(len(string1)):
            if(string1[x] != string2[x]):
                break
            else:
                count = count + 1

        return count

    def getSrcPortNumber(self,alert):
        port = 0
        if(alert.tcp_sport != "Tidak menggunakan TCP"):
            port = alert.tcp_sport
        else:
            port = alert.udp_sport
        return port

    def compareIP(self,ipAddr1,ipAddr2):

        ipBin1 = self.ipToBinary(ipAddr1)
        ipBin2 = self.ipToBinary(ipAddr2)
        
        return self.compareUrutan(ipBin1,ipBin2)

    def compareNumber(self,num1,num2):
        if (num1 == num2):
            return 1
        else:
            return 0

    def calculateF1(self):
        ip_src1 = self.alert1.ip_src
        ip_src2 = self.alert2.ip_src
        return self.compareIP(ip_src1,ip_src2)/32
        
    def calculateF2(self):
        ip_dst1 = self.alert1.ip_dst
        ip_dst2 = self.alert2.ip_dst
        return self.compareIP(ip_dst1,ip_dst2)/32        

    def calculateF3(self):
        src_port1 = self.getSrcPortNumber(self.alert1)
        src_port2 = self.getSrcPortNumber(self.alert2)
        return self.compareNumber(src_port1,src_port2)

    def calculateF4(self):
        ip_src1 = self.alert1.ip_src
        ip_dst2 = self.alert2.ip_dst
        return self.compareNumber(ip_src1,ip_dst2)

    def calculateF5(self):
        value = 0
       
        if(self.f1 == self.f2 == self.f3 == 1):
            value = 1

        return value

    
    def calculateF6(self):
        time1 = self.alert1.timestamp
        time1 = time.mktime(time.strptime(time1, "%Y-%m-%d %H:%M:%S"))
        # print "alert1 : "+str(time1)

        time2 = self.alert2.timestamp
        time2 = time.mktime(time.strptime(time2, "%Y-%m-%d %H:%M:%S"))
        # print "alert2 : "+str(time2)

        deltaTime = abs(time1-time2)
        if(deltaTime == 0):
            frequency = 1/1
        else :
            frequency = 1/(deltaTime)
        
        return frequency

    def getValues(self):
        newList = []
        newList.append(self.f1)
        newList.append(self.f2)
        newList.append(self.f3)
        newList.append(self.f4)
        newList.append(self.f5)
        newList.append(self.f6)
        return newList

class TimeFrame:
    startTime   = 0
    endTime     = 0
    
    def __init__(self,firstTime,lastTime):
        self.startTime  = firstTime
        self.endTime    = lastTime
        self.alerts     = []

    def appendNewAlert(self,newAlert):
        self.alerts.append(newAlert)

class AlertCausalityMatrix:
    causalityMatrix = []
    alertList       = []
    alertSigmaValue = []

    def __init__(self,newAlertList):
        self.alertList = newAlertList
        for i in range(len(self.alertList)):
            tempList = []
            self.alertSigmaValue.append(0)    
            for j in range(len(self.alertList)):
                tempList.append(0)

            self.causalityMatrix.append(tempList)
        


    def getAlertIndex(self,alertName):
        
        if ((alertName in self.alertList) == True):
            index = self.alertList.index(alertName)
        else:
            index = -1

        return index

    def incrementACMValue(self,alert1,alert2):

        index1 = self.getAlertIndex(alert1)
        index2 = self.getAlertIndex(alert2)
        if (index1 != -1 and index2 != -1):
            self.causalityMatrix[index1][index2] = self.causalityMatrix[index1][index2] + 1

    def calculateAllSigmaValue(self):
        
        for i in range(len(self.alertList)):
            self.alertSigmaValue[i] = 0

        for i in range(len(self.alertList)):
            for j in range(len(self.alertList)):
               self.alertSigmaValue[i] += self.causalityMatrix[i][j] 

    def calculateForwardCorrelationStrength(self,alert1,alert2):
        index1 = self.getAlertIndex(alert1)
        index2 = self.getAlertIndex(alert2)
        value = self.causalityMatrix[index1][index2]/self.alertSigmaValue[index1]
        return value

    def getRelatedList(self):
        self.calculateAllSigmaValue()
        edgeList = []
        for i in range(len(self.alertList)):
            maxValue = 0
            
            for j in range(len(self.alertList)):

                alert1 = self.alertList[i]
                alert2 = self.alertList[j]
                forwardCorrelation = self.calculateForwardCorrelationStrength(alert1,alert2)
                if maxValue < forwardCorrelation:
                    maxValue = forwardCorrelation
            
            for j in range(len(self.alertList)):

                alert1 = self.alertList[i]
                alert2 = self.alertList[j]
                forwardCorrelation = self.calculateForwardCorrelationStrength(alert1,alert2)
                if(maxValue - forwardCorrelation <= 0.3 and forwardCorrelation != 0):
                    edge = {(alert1,alert2):forwardCorrelation}
                    edgeList.append(edge)
                output = "maxValue : "+str(maxValue)+" FCStrength : "+str(forwardCorrelation)+"\n"
                # print output

        return edgeList

# "1","2000-03-07 06:51:36","172.16.115.1","202.77.162.213","Ya","8","Tidak menggunakan TCP","Tidak menggunakan TCP","Tidak menggunakan UDP","Tidak menggunakan UDP","ICMP PING","misc-activity"
# "2","2000-03-07 06:51:36","202.77.162.213","172.16.115.1","Ya","0","Tidak menggunakan TCP","Tidak menggunakan TCP","Tidak menggunakan UDP","Tidak menggunakan UDP","ICMP Echo Reply","misc-activity"