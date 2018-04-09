from __future__ import division


class Alert:
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
        self.udp_dport      = file_tcp_dport
        self.udp_sport      = file_tcp_sport
        self.sig_name       = file_sig_name
        self.sig_class_name = file_sig_class_name
        self.phase          = file_phase

    def getTimestamp(self):
        return self.timestamp

class AlertCorrelation:
    alerts  = []
    f1      = 0
    f2      = 0
    f3      = 0
    f4      = 0

    def __init__(self,alert1,alert2):
        self.alerts.append(alert1)
        self.alerts.append(alert2)

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
            if(string1[x] == string2[x]):
                count = count + 1

        return count

    def compareIP(self,ipAddr1,ipAddr2):

        ipBin1 = self.ipToBinary(ipAddr1)
        ipBin2 = self.ipToBinary(ipAddr2)
        
        return self.compareUrutan(ipBin1,ipBin2)

    def calculateF1(self):
        ip_src1 = self.alerts[0].ip_src
        ip_src2 = self.alerts[1].ip_src
        return self.compareIP(ip_src1,ip_src2)/32
        
    def calculateF2(self,ip_dst1,ip_dst2):
        return self.compareIP(ip_dst1,ip_dst2)/32

    # def calculateF3():
    #     ports1 = []
    #     if (alerts[1].icmp_status == "Ya"):
    #         if(alerts[1].tcp_dport != "Tidak menggunakan TCP"):
    #     else:

