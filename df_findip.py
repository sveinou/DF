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
		"""
		Parses leasefile and returns mac-addresses
		"""

		file = open(self.leasefile)
		text = file.read()
		regex_mac = re.compile(self.mac_filter)
		return regex_mac.findall(text)

	def ip_exists(self, ip_address):
		"""
		Checks if ip_address exists in dhcp leasetable
		"""
		return ip_address in self.get_ips()

	def mac_exists(self, mac_address):
		"""
		Checks if mac_address exists in dhcp leasetable
		"""
		return mac_address in self.get_macs()

	def get_mac(self, ip_address):
		"""
		Searches for ip_address and returnes mac-address
		raises KeyError
		"""
		return self.get_leases()[ip_address]

	def get_leases(self):
		"""
		Returns dict with pairs of mac's and ip-addresses from dhcp-table
		"""
		return dict(zip(self.get_ips(),self.get_macs()))

