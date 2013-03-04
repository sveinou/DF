import re        # regexp
import conf     # most settings exists in conf.py

class DHCP:
    """
    Checks leases in dhcp
    """
    
    def __init__(self, leasefile):
        if leasefile == None:
            leasefile = conf.files.leasefile
        elif type(leasefile) != str:
            raise ValueError("No leasefile given!")
        self.leasefile = leasefile
#    ip_filter = r'([\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3})'
#    mac_filter = r'([a-f|0-9][a-f|0-9]\:[a-f|0-9][a-f|0-9]\:[a-f|0-9][a-f|0-9]\:[a-f|0-9][a-f|0-9]\:[a-f|0-9][a-f|0-9]\:[a-f|0-9][a-f|0-9])' 

    def get_ips(self):
        """ 
        Parses leasefile  and returns list of registered ip-adresses
        """
        file = open(self.leasefile)
        text = file.read()
        regex_ip = re.compile(conf.filter.ipv4_in_leasefile)
        return regex_ip.findall(text)

    def get_macs(self):
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
