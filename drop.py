#!/usr/bin/python

import re
import conf
from df_firewall import Firewall
from df_data import Data
from logger import Log
class Drop:
    """
    Does magic stuff.
    """
    
    def __init__(self):
        pass
        self.log = Log(conf.files.droplog)

    def ip4(self,ip):
        """
        Drops IPv4 address from iptables and database
        """
        checkip = re.compile(conf.filter.ipv4_exact)
        if checkip.match(ip) == None:
            print "Invalid IP:\n"+ip
            exit(conf.exit_status.input_error)
        
        firewall = Firewall()
        data = Data()

        self.log.info("DROPPED: "+ip)
        firewall.drop_ip4(ip)
        data.DbActiveIp4(ip,0)
		
    def drop_ip6(self,ip):
        print "IPv6 not yet implemented."

