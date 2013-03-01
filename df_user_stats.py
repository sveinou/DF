
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
		ipct = open(/proc/net/ip_conntrack).read().split("\n")
		return [line for line in iptc if line.find(self.ip) > 0] #add lines with self.ip to my-list.
		
		

		
				
