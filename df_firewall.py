import subprocess

class Firewall:
    """
    Sends commands to iptables to alter chains
    """

    def __init__(self):
        pass

    def accept_ip4(self, ipv4_addr):
        """
        Opens iptables FORWARD and PRERPOUTING chain for ipaddress
        
        Keywords arguments:
        ipv4_addr -- IPv4-address to let trough firewall
        """
         
        rules = ["/sbin/iptables -I FORWARD -d"+ipv4_addr+" -j ACCEPT",
            "/sbin/iptables -I FORWARD -s"+ipv4_addr+" -j ACCEPT",
            "/sbin/iptables -t nat -I PREROUTING -d"+ipv4_addr+" -j ACCEPT",
            "/sbin/iptables -t nat -I PREROUTING -s"+ipv4_addr+" -j ACCEPT",]
 
        for rule in rules:
            subprocess.call(rule, shell=True)


    def accept_ip6(self, ipv6_addr):
        """
        Tells iptables to let trough IPv6-addess
        
        Keyword Arguments:
        ipv6_addr -- IPv6-address that's welcome trough our firewall
        """
        
        rules = ["/sbin/iptables -I FORWARD -d"+ipv6_addr+" -j ACCEPT",
			"/sbin/iptables -I FORWARD -s"+ip6_addr+" -j ACCEPT",]
        for rule in rules:
            subprocess.call(rule, shell=True)


    def drop_ip4(self, ipv4_addr):
        """
        Removes ip-address from accept-list
        
        Keyword arguments:
        ipv4_addr = IPv4-address to remove
        """
        
        rules = ["/sbin/iptables -D FORWARD -d"+ipv4_addr+" -j ACCEPT",
            "/sbin/iptables -D FORWARD -s"+ipv4_addr+" -j ACCEPT",
            "/sbin/iptables -t nat -D PREROUTING -d"+ipv4_addr+" -j ACCEPT",
            "/sbin/iptables -t nat -D PREROUTING -s"+ipv4_addr+" -j ACCEPT",]

        for rule in rules:
            subprocess.call(rule, shell=True)

    def drop_ip6(self, ipv6_addr):
        """
        Removes ipv6-address from iptables accept-list
        
        Keyword arguments:
        ipv6_addr = IPv6 address to remove
        """
        
        rules = ["/sbin/ip6tables -D FORWARD -d"+ipv6_addr+" -j ACCEPT",
            "/sbin/ip6tables -D FORWARD -s"+ipv6_addr+" -j ACCEPT",]

        for rule in rules:
            subprocess.call(rule, shell=True)   
	
	
	
		


	def isRule(ip):
	"""
	Returns true if there is an rule with given ip-addres, 
	if the rule do not exist, it wil return false
	"""

        	ip6 = subprocess.check_output("/sbin/ip6tables -L -n", shell=True)

        	ip4 = subprocess.check_output("/sbin/iptables -L -n", shell=True)
        	ip4_nat = subprocess.check_output("/sbin/iptables -t nat -L -n ", she$

        	if ip in ip4 or ip in ip6 or ip in ip4_nat:
                	return(True)
        	else:
                	return(False)	

	

