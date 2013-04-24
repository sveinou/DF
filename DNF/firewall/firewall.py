import subprocess
from DNF.database.df_data import Data
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
         
        rules = ["/sbin/iptables -I ALLOWED -d"+ipv4_addr+" -j ACCEPT",
            "/sbin/iptables -I ALLOWED -s"+ipv4_addr+" -j ACCEPT",
            "/sbin/iptables -t nat -I ALLOWED -d"+ipv4_addr+" -j ACCEPT",
            "/sbin/iptables -t nat -I ALLOWED -s"+ipv4_addr+" -j ACCEPT",]
 
        for rule in rules:
            subprocess.call('sudo '+rule, shell=True)


    def accept_ip6(self, ipv6_addr):
        """
        Tells iptables to let trough IPv6-addess
        
        Keyword Arguments:
        ipv6_addr -- IPv6-address that's welcome trough our firewall
        """
        
        rules = ["/sbin/iptables -I ALLOWED -d"+ipv6_addr+" -j ACCEPT",
  		"/sbin/iptables -I ALLOWED -s"+ipv6_addr+" -j ACCEPT",]
        for rule in rules:
            subprocess.call('sudo '+ rule, shell=True)


    def drop_ip4(self, ipv4_addr):
        """
        Removes ip-address from accept-list
        
        Keyword arguments:
        ipv4_addr = IPv4-address to remove
        """
        
        rules = ["/sbin/iptables -D ALLOWED -d"+ipv4_addr+" -j ACCEPT",
            "/sbin/iptables -D ALLOWED -s"+ipv4_addr+" -j ACCEPT",
            "/sbin/iptables -t nat -D ALLOWED -d"+ipv4_addr+" -j ACCEPT",
            "/sbin/iptables -t nat -D ALLOWED -s"+ipv4_addr+" -j ACCEPT",]

        for rule in rules:
            subprocess.call('sudo ' + rule, shell=True)

    def drop_ip6(self, ipv6_addr):
        """
        Removes ipv6-address from iptables accept-list
        
        Keyword arguments:
        ipv6_addr = IPv6 address to remove
        """
        
        rules = ["/sbin/ip6tables -D ALLOWED -d"+ipv6_addr+" -j ACCEPT",
            "/sbin/ip6tables -D ALLOWED -s"+ipv6_addr+" -j ACCEPT",]

        for rule in rules:
            subprocess.call('sudo '+rule, shell=True)   


    def limit_connections(self, ip):
        """
        Adds connectionlimit to user
        """
        rules = ["iptables -I LIMITED -d "+ip+" -j LIMIT",
                 "iptables -I LIMITED -s "+ip+" -j LIMIT"]
        
        for rule in rules:
            subprocess.call('sudo ' + rule, shell=True)   

        
        #update something in the database?
        
        return


    def is_rule(self, ip): #isRule
        """
        Returns true if there is an rule with given ip-addres, 
        if the rule do not exist, it wil return false
        """
        ip6 = subprocess.check_output("sudo /sbin/ip6tables -L -n", shell=True)

        ip4 = subprocess.check_output("sudo /sbin/iptables -L -n", shell=True)
        ip4_nat = subprocess.check_output("sudo /sbin/iptables -t nat -L -n ", shell=True)

        if ip in ip4 or ip in ip6 or ip in ip4_nat:
            return True
        else:
            return False
        
    def get_custom_forward(self):
        """
        returns all rules in limited-chain.        
        """
        ipcmd = ['sudo', 'iptables', '-nvxL', 'CUSTOM_FORWARD']
        ipres  = subprocess.Popen(ipcmd, stdout=subprocess.PIPE).communicate()[0].split("\n")
        return [line.split() for line in ipres[2:-1]]
    def get_custom_input(self):
        """
        returns all rules in limited-chain.        
        """
        ipcmd = ['sudo', 'iptables', '-nvxL', 'CUSTOM_INPUT']
        ipres  = subprocess.Popen(ipcmd, stdout=subprocess.PIPE).communicate()[0].split("\n")
        return [line.split() for line in ipres[2:-1]]
    
    def get_limited(self):
        """
        returns all rules in limited-chain.        
        """
        ipcmd = ['sudo', 'iptables', '-nvxL', 'LIMITED']
        ipres  = subprocess.Popen(ipcmd, stdout=subprocess.PIPE).communicate()[0].split("\n")
        return [line.split() for line in ipres[2:-1]]
    
    def get_allowed(self):
        """
        Returns all rules in allowed-chain
        """
        ipcmd = ['sudo', 'iptables', '-nvxL', 'ALLOWED']
        ipres  = subprocess.Popen(ipcmd, stdout=subprocess.PIPE).communicate()[0].split("\n")
        return [line.split() for line in ipres[2:-1]]


    def rm_limit(self, ip):

	ipt = subprocess.Popen(["iptables","-L", "LIMITED"], stdout = subprocess.PIPE)
	grep = subprocess.Popen(["grep", ip], stdin=ipt.stdout, stdout = subprocess.PIPE)
	out = grep.communicate()[0]
	for rule in out.split("\n"):
		rule = rule.split("all")[0]
		print rule
		if rule == "RXLIMIT":
			subprocess.call("iptables -D LIMITED -d "+ip+" -j "+rule, shell=True)
		elif rule == "TXLIMIT":
			subprocess.call("iptables -D LIMITED -s "+ip+" -j "+rule, shell=True)
		else: # will try to remove tvice as manny rules as there are,
			subprocess.call("iptables -D LIMITED -s "+ip+" -j "+rule, shell=True)
			subprocess.call("iptables -D LIMITED -d "+ip+" -j "+rule, shell=True) 

	Data().rm_limit(ip)
        return
    def rm_all_limit(self):
    	subprocess.call("iptables -F LIMITED", shell=True)
    	Data().rm_all_limit()
    	
        

    def limit_rx(self, ip):
	if not Firewall().is_rule(ip,"LIMITED","RXLIMIT"):
	    subprocess.call("iptables -I LIMITED -d "+ip+" -j RXLIMIT", shell=True) 
	    Data().add_limit(ip,"RXLIMIT")
	return

    def limit_tx(self, ip):
	if not Firewall().is_rule(ip,"LIMITED","TXLIMIT"):
	    subprocess.call("iptables -I LIMITED -s "+ip+" -j TXLIMIT", shell=True) 
	    Data().add_limit(ip,"TXLIMIT")
	return
