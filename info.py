import conf
import re
from df_data import Data 
from df_findip import DHCP
from df_user_stats import Statistics
import conf, re, sys

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

	
        if type(ip) != str:
            raise ValueError("User not string!")

        else:
            return {'ipv4_addr':ip}

	
    def isLoggedIn(self,ip):
        ip = self.check_input(ip)
        return Data().isActiveIp4(ip) and DHCP(None).ip_exists(ip)

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

User is currently {6}""".format(ip,connections,io['bytes_sent'],io['pkt_sent'],io['bytes_received'],io['pkt_received'], active)


