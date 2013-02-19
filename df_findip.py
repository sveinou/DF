import re	# regexp

class DHCP:
	"""
	Checks leases in dhcp
	"""
	
	# We should probably make a configuration-file... 
	leasefile = '/var/lib/dhcp/dhcpd.leases'
	ip_filter = r'([\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3})'
	mac_filter = r'([a-f|0-9][a-f|0-9]\:[a-f|0-9][a-f|0-9]\:[a-f|0-9][a-f|0-9]\:[a-f|0-9][a-f|0-9]\:[a-f|0-9][a-f|0-9]\:[a-f|0-9][a-f|0-9])' 

	def get_ips(self):
		""" 
		parses lease-file in \"leasefile\" and returns list of registered ip-adresses
		"""
		file = open(self.leasefile)
		text = file.read()
		regex_ip = re.compile(self.ip_filter)
		return regex_ip.findall(text)

	def get_macs(self):
		file = open(self.leasefile)
		text = file.read()
		regex_mac = re.compile(self.mac_filter)
		return regex_mac.findall(text)


	def ip_exists(self, ip_address):
		return ip_address in self.get_ips()

	def get_leases(self):
		return dict(zip(self.get_macs(),self.get_ips()))

	def print_leases(self):
		"""	
		Prints out found leases
		"""
		leases = self.get_leases()
		print "Number of leases: ",len(leases)
		for lease in leases:
			print lease.key, ": ",lease.value

