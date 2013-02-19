import re	# regexp

class DHCP:
	"""
	Checks leases in dhcp
	"""
	
	# We should probably make a configuration-file... 
	leasefile = '/var/lib/dhcp/dhcpd.leases'
	ip_filter = r'([\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3})'
	#ip_filter = r'^lease\ [\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\ \{$'
	#regex_mac = r'([a-f|0-9][a-f|0-9]\:[a-f|0-9][a-f|0-9]\:[a-f|0-9][a-f|0-9]\:[a-f|0-9][a-f|0-9]\:[a-f|0-9][a-f|0-9]\:[a-f|0-9][a-f|0-9])' 

	def get_leases(self):
		""" 
		parses lease-file in \"leasefile\" and returns list of registered ip-adresses
		"""
		file = open(self.leasefile)
		text = file.read()
		regex_ip = re.compile(self.ip_filter)
		return regex_ip.findall(text)


	def print_leases(self):
		"""	
		Prints out found leases
		"""
		leases = self.get_leases()
		print "Number of leases: ",len(leases)
		for lease in leases:
			print "IP: "+lease

