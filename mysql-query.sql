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


-- cid,timestamp,sig_name,sig_class_name
SELECT
	e.cid as cid,
	e.timestamp as timestamp,
	e.ip_dst as ip_dst,
	e.ip_src as ip_src,	
	e.icmp as icmp,
	e.icmp_type as icmp_type,
	e.tcp_dport as tcp_dport,
	e.tcp_sport as tcp_sport,
	u.udp_dport as udp_dport,
	u.udp_sport as udp_sport,
	e.sig_name as sig_name,
	e.sig_class_name as sig_class_name
FROM
	(SELECT
		e.cid as cid,
		e.timestamp as timestamp,
		e.ip_dst as ip_dst,
		e.ip_src as ip_src,
		e.sig_name as sig_name,
		e.sig_class_name as sig_class_name,	
		e.icmp as icmp,
		e.icmp_type as icmp_type,
		t.tcp_dport as tcp_dport,
		t.tcp_sport as tcp_sport
	FROM
		(SELECT
			e.cid as cid,
			e.timestamp as timestamp,
			e.ip_dst as ip_dst,
			e.ip_src as ip_src,
			e.sig_name as sig_name,
			e.sig_class_name as sig_class_name,
			i.icmp as icmp,
			i.icmp_type as icmp_type
		FROM
			(SELECT
				s.cid as cid, 
				s.timestamp as timestamp, 
				s.sig_name as sig_name, 
				s.sig_class_name as sig_class_name, 
				inet_ntoa(i.ip_dst) as ip_dst, 
				inet_ntoa(i.ip_src) as ip_src
			FROM 	
				(select 
					s.cid as cid, 
					s.timestamp as timestamp, 
					s.sig_name as sig_name, 
					sc.sig_class_name as sig_class_name
				FROM
					(select 
						e.cid as cid, 
						e.timestamp as timestamp, 
						s.sig_name as sig_name,  
						s.sig_class_id as sig_class_id 
					from event e, signature s
					where e.signature = s.sig_id) s, 
					sig_class sc
				where s.sig_class_id = sc.sig_class_id) s, 
				iphdr i
			WHERE s.cid = i.cid) e,
			(SELECT
				e.cid as cid, 
				CASE IFNULL(i.cid,-1)
				WHEN -1 THEN 'Tidak menggunakan ICMP'
				ELSE 'Ya'
				END as icmp,
				CASE IFNULL(i.icmp_type,-1)
				WHEN -1 THEN 'Tidak menggunakan ICMP'
				ELSE i.icmp_type 
				END as icmp_type
			FROM event e
			LEFT JOIN icmphdr i ON e.cid = i.cid) i
		WHERE e.cid = i.cid) e,
		(SELECT
			e.cid,
			CASE IFNULL(t.tcp_dport,-1)
			WHEN -1 THEN 'Tidak menggunakan TCP'
			ELSE t.tcp_dport
			END as tcp_dport,
			CASE IFNULL(t.tcp_sport,-1)
			WHEN -1 THEN 'Tidak menggunakan TCP'
			ELSE t.tcp_sport
			END as tcp_sport
		FROM event e
		LEFT JOIN tcphdr t ON e.cid = t.cid) t
	WHERE e.cid = t.cid) e,
	(SELECT
		e.cid,
		CASE IFNULL(u.udp_dport,-1)
		WHEN -1 THEN 'Tidak menggunakan UDP'
		ELSE u.udp_dport
		END as udp_dport,
		CASE IFNULL(u.udp_sport,-1)
		WHEN -1 THEN 'Tidak menggunakan UDP'
		ELSE u.udp_sport
		END as udp_sport
	FROM event e
	LEFT JOIN udphdr u ON e.cid = u.cid) u
WHERE e.cid = u.cid
ORDER BY e.cid;