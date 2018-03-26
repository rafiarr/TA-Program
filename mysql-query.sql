-- non-icmp query :
select a.sig_class_name as attack, i.ip_src as ip_src, i.udp_sport as sport, i.ip_dst as ip_dst, i.udp_dport as dport, i.timestamp as timestamp 
from 	(SELECT i.cid as cid, i.signature as signature, i.timestamp as timestamp, i.ip_src as ip_src, i.ip_dst as ip_dst, u.udp_sport as udp_sport, u.udp_dport as 	 udp_dport 
	from 	(select e.cid as cid, e.signature as signature, e.timestamp as timestamp, inet_ntoa(i.ip_src) as ip_src, inet_ntoa(i.ip_dst) as ip_dst, i.ip_proto as 		 ip_proto 
		 from event e, iphdr i 
		 where e.cid = i.cid) i, udphdr u 
	where i.cid = u.cid and i.ip_proto != 1) i, 
	(select s.sig_id as signature, c.sig_class_name as sig_class_name 
	 from sig_class c, signature s 
	 where (s.sig_id = 511 or s.sig_id = 509) and c.sig_class_id = s.sig_class_id) a 
where i.signature=a.signature order by i.timestamp;

-- icmp query :
select a.sig_class_name as attack, i.ip_src as ip_src, i.sport as sport, i.ip_dst as ip_dst, i.dport as dport, i.timestamp as timestamp 
from 	(select e.cid as cid, e.signature as signature, e.timestamp as timestamp, inet_ntoa(i.ip_src) as ip_src, inet_ntoa(i.ip_dst) as ip_dst, i.ip_proto as ip_proto, 	 0 as sport, 0 as dport 
	 from event e, iphdr i 
	 where e.cid = i.cid and i.ip_proto = 1) i, 
	(select s.sig_id as signature, c.sig_class_name as sig_class_name 
	 from sig_class c, signature s 
	 where (s.sig_id = 511 or s.sig_id = 509) and c.sig_class_id = s.sig_class_id) a 
where i.signature=a.signature order by i.timestamp;

-- requirement : cid, timestamp, ip_src, ip_dst, tcp_sport, tcp_dport, udp_sport, udp_dport, sig_name, sig_class_name, icmp_activity, icmp_type