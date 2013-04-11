from DNF import conf
from DNF.database.df_data import Data 
from DNF.stats.df_user_stats import Statistics
import re, sys

class Dhcp:

    def __init__(self, leasefile=conf.files.leasefile):
        self.leasefile = leasefile

    def read_leases(self):
        leases = open(self.leasefile).read().split('\n}')
        leases[0] = leases[0][leases[0].find('\nlease '):] #Cleaning first entry in file
        
        return [Lease(lease) for lease in leases]
        
    def find_mac(self, ip):
        
        for lease in self.read_leases():
            if lease.ip == ip:
                return lease.mac
        return False
        
    def get_lease(self, ip):
        pass
        

class Lease:       
    ip = ''
    mac = ''

    def __init__(self, fromleasefile):
        ipcheck = re.compile(conf.filter.ipv4_in_leasefile)
        maccheck = re.compile(conf.filter.mac_in_leasefile)
        ip = ipcheck.findall(fromleasefile) 
        if ip:
            self.ip = ip[0][1:]
        mac = maccheck.findall(fromleasefile)
        if mac:
            self.mac = mac[0]
#        lease = fromleasefile.split('\n')
#        ip = lease[1][6:-2]
#        if lease[7].find('hardware ethernet') > 0:
#            mac = lease[7][-18:-1]
#        else:
#            mac = "Not Available"    

class System:
    
    def connection_load(self):
        return len(open(conf.files.ip_conntrack).read().split("\n"))
    
class IP():
    def check_input(self, ip):
        ipcheck = re.compile(conf.filter.ipv4_exact)
        if ipcheck.match(ip) == None:
            raise ValueError("Not IPv4 addr")	
        return ip

#        if type(ip) != str:
#            raise ValueError("User not string!")
#        else:
#            return {'ipv4_addr':ip}


    def isLoggedIn(self,ip):
        ip = self.check_input(ip)
        active = Data().active('ip4', ip)
        exists = Leasefile().ip_exists(ip)
        print("%s: A:%s, E:%s" % (ip,active,exists))
        return active and exists

##      this should be named print_stats
    def getStats(self,ip):
        ip = self.check_input(ip);
        
        s = Statistics()
        connections = s.get_active_connections(ip)
        io = s.get_iptables_io(ip)
        
        active = "NOT ACTIVE"
        if self.isLoggedIn(ip):
            active = "ACTIVE"
        return """Statistics for {0} 
Active Connections: {1}
Sent {2} bytes using {3} packets
Received {4} bytes using {5} packets

User is currently {6}""".format(ip, connections, io['bytes_sent'], io['pkt_sent'], io['bytes_received'], io['pkt_received'], active)

class Leasefile:
    """
    Checks leases in dhcp
    """
    
    def __init__(self, leasefile=conf.files.leasefile):
        self.leasefile = leasefile

    def get_ips(self):
        """ 
        Parses leasefile  and returns list of registered ip-adresses
        """
        file = open(self.leasefile)
        text = file.read()
        regex_ip = re.compile(conf.filter.ipv4_in_leasefile)
        return [ip.strip() for ip in regex_ip.findall(text)]

        """
        Parses leasefile and returns mac-addresses
        """

        file = open(self.leasefile)
        text = file.read()
        regex_mac = re.compile(conf.filter.mac_in_leasefile)
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
        --- returns None if ip does not exist
        """
        if self.ip_exists(ip_address):
            return self.get_leases()[ip_address]
        return None
            
    def get_leases(self):
        """
        Returns dict with pairs of mac's and ip-addresses from dhcp-table
        """
        return dict(zip(self.get_ips(),self.get_macs()))

    def get_ipv4_lease(self, ipv4_addr):
        """
        Retrurns tuple with (ip,mac) or None if does not exist
        """
        mac_addr = self.get_mac(ipv4_addr)
        if not self.ip_exists(ipv4_addr) or mac_addr == None:
            return None

        return (ipv4_addr, mac_addr)

    def is_ipv4(self, address):
        """
        Checks address to IPv4-filter
        """
        test = re.compile(conf.filter.ipv4_exact)
        if(test.match(address) != None):
            return True

        return False
