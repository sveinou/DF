import conf


class Statistics:
	"""
	Shows statistics based on ip_address
	"""
	
	def __init__(self, ipv4_addr):
		self.ip = ipv4_addr

	
	def get_conntrack(self):
		"""
		Returns list of ip_conntrack entries of self.ip
		"""
		ipct = open(conf.files.ip_conntrack).read().split("\n")
		return [line for line in ipct if line.find(self.ip) > 0] #add lines with self.ip to my-list.
		
		
	def get_bytes_io(self):
		"""
		Counts bytes form ip_conntrack and returns tuple with (sendt,recived) bytes
		"""

		iptc = self.get_conntrack()		
		tx = 0;
		rx = 0;
		tx_tcp = [line.split(" ")[14][6:] for line in iptc if line.split(" ")[0] == 'tcp']	##TCP
		tx_udp = [line.split(" ")[13][6:] for line in iptc if line.split(" ")[0] == 'udp']	##UDP		
		rx_tcp = [line.split(" ")[-5][6:] for line in iptc if line.split(" ")[0] == 'tcp']	##TCP
		rx_udp = [line.split(" ")[-4][6:] for line in iptc if line.split(" ")[0] == 'udp']	##UDP		

		for t in tx_tcp:
			tx += int(t)
		for u in tx_udp:
			tx += int(u)
		for t in rx_tcp:
			rx += int(t)
		for u in rx_udp:
			rx += int(u)

		return (tx,rx)

