#!/usr/bin/python

import re, logging
from DNF import conf
from DNF.firewall.firewall import Firewall
from DNF.database.df_data import Data
class Drop:
    """
    Does magic stuff.
    """
    
    log = logging.getLogger(__name__)
    log.addHandler(conf.log.users)
    #log.addFilter(conf.log.logformat)
    log.setLevel(conf.log.level)
    
    def __init__(self):
        pass

    def ip4(self,ip):
        """
        Drops IPv4 address from iptables and database
        """
        checkip = re.compile(conf.filter.ipv4_exact)
        if checkip.match(ip) == None:
            print "Invalid IP:\n"+ip
            self.log.error("Tried to drop invalid IP %s" % ip)
            exit(conf.exit_status.input_error)
        
        firewall = Firewall()
        data = Data()

        self.log.info("DROPPED: "+ip)
        firewall.drop_ip4(ip)
        data.active_ip4(ip,0)


    def drop_ip6(self,ip):
        print "IPv6 not yet implemented."

