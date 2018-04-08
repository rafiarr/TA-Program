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
