class Alert:
    def __init__(self,timestamp,ip_dst,ip_src,icmp,icmp_type,tcp_dport,tcp_sport,udp_dport,udp_sport,sig_name,sig_class_name):
        self.timestamp      = timestamp
        self.ip_dst         = ip_dst
        self.ip_src         = ip_src
        self.icmp           = icmp
        self.icmp_type      = icmp_type
        self.tcp_dport      = tcp_dport
        self.tcp_sport      = tcp_sport
        self.udp_dport      = tcp_dport
        self.udp_sport      = tcp_sport
        self.sig_name       = sig_name
        self.sig_class_name = sig_class_name

    def getTimestamp(self):
        return self.timestamp

alert1 = Alert("2000-03-07 06:51:36","172.16.115.1","202.77.162.213","Ya","8","Tidak menggunakan TCP","Tidak menggunakan TCP","Tidak menggunakan UDP","Tidak menggunakan UDP","ICMP PING","misc-activity")