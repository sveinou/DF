from DNF import conf
import subprocess as sp
from DNF.firewall.firewall import Firewall
import time, logging


class Statistics:
    """
    Shows statistics based on ip_address
    """
    
    log = logging.getLogger(__name__)
    log.addHandler(conf.log.users)
#    log.addFilter(conf.log.logformat)
    log.setLevel(conf.log.level)
    
    def __init__(self):
        pass
    
    @DeprecationWarning
    def get_conntrack(self, ip):
        """
        Returns list of ip_conntrack entries of self.ip
        """
        #ipct = open(conf.files.ip_conntrack, mode='r').read().split("\n")
        #return [line for line in ipct if line.find(ip) > 0] #add lines with self.ip to my-list.
        return self.get_connections(ip)
    
    def get_connections(self, ip):
        cmd = ['netstat', '--ip', ip]
        res  = sp.Popen(cmd, stdout=sp.PIPE).communicate()[0].split("\n")
        return res[2:]

    def get_active_connections(self, ip):
        """
        Returns number of active connections to self.ip
        """
        #return len(self.get_conntrack(ip))
        return len(self.get_connections(ip))
    
    def is_limited(self, ip):
        """
        Returns True if IP is in iptables limted-chain
        """
        return ip in [rule[7] for rule in Firewall().get_limited()]
    
    def is_allowed(self, ip):
        """
        Returns True if IP is in iptables allowed-chain
        """
        return ip in [rule[7] for rule in Firewall().get_allowed()]

    def get_iptables_io(self, ip):
        """
        Executes call to iptables and filters out info about ip

        Returns dictionary with following info:
            pkt_sent = Packages sent from self.ip (int)
            pkt_received = Packages recieved to self.ip (int)
            bytes_sent  = Bytes sent from self.ip (int)
            bytes_received = Bytes received to self.ip (int)
        """
        ipcmd = ['sudo', '/sbin/iptables', '-nvxL', 'ALLOWED']
        ipres  = sp.Popen(ipcmd, stdout=sp.PIPE).communicate()[0].split("\n")
        res = [line for line in ipres if line.find(ip) > 0]

        if res:
            tx_pkts = int(res[0].split(*'')[0])
            rx_pkts = int(res[1].split(*'')[0])
            tx_bytes = int(res[0].split(*'')[1])
            rx_bytes = int(res[1].split(*'')[1])

            return {'pkt_sent':tx_pkts, 'pkt_received':rx_pkts, 'bytes_sent':tx_bytes, 'bytes_received':rx_bytes}
        else:
            self.log.error("df_user_stats.py: Something wrong with iptables-lookup...: "+ip)
            return {'pkt_sent':0, 'pkt_received':0, 'bytes_sent':0, 'bytes_received':0}

    def get_all_io(self, ips, io=[]):
	"""
	this wil get the stats from all the clients
	then w8 10 seconds to get them again
	it will then have an good idea about txs and rxs
	"""
	i = 0
        clients_bytes = []
     
        for ip in ips:
            ipcmd = ['iptables', '-nvxL', 'ALLOWED']
            ipres = sp.Popen(ipcmd, stdout=sp.PIPE).communicate()[0].split("\n")
            res = [line for line in ipres if line.find(ip) > 0]
     
        if res and not io:
            tx_bytes = int(res[0].split(*'')[1])
            rx_bytes = int(res[1].split(*'')[1])
            clients_bytes += [[tx_bytes, rx_bytes]]
     
        elif res and io:  # will not work if the ip do not exsit!!
            tx_after = int(res[0].split(*'')[1])
            rx_after = int(res[1].split(*'')[1])
            tx_before = io[i][0]
            rx_before = io[i][1]
            txs = (tx_after - tx_before) / 10
            rxs = (rx_after - rx_before) / 10
            clients_bytes += [[ip, txs, rxs]]
     
        i += 1
        if not io:
            time.sleep(10)
     
        return self.get_all_io(ips, clients_bytes) if not io else clients_bytes

