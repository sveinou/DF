#!/usr/bin/python

import subprocess
import sys
import re
import conf
from df_firewall import Firewall
from df_data import Data

def get_input():
    """
    Gets username and IP-address from commandline
    and pases it on as dictionary.
    """
    argv = sys.argv
    if len(argv) == 3:

        user = argv[1]
        ip = argv[2]
        if type(user) != str:	
            raise ValueError("User not string!")
        elif type(ip) != str or len(ip) < 7:
	        raise ValueError("error on IP input")
	
        return {'username':user, 'ip_addr':ip}

    elif len(argv) == 2:
        ip = argv[1]
        f = re.compile(conf.filter.ipv4_exact)
        if(f.match(ip) == None):
            raise ValueError("Not an IPv4-address");
        return {'ip_addr':ip}


    else:
        raise ValueError("Not enough/Too many arguments")

    


def main():
    indata = get_input()
    ip = indata['ip_addr']
    firewall = Firewall()
    data = Data()

    if len(ip) > 15:            # We should use filters!
        firewall.drop_ip6(ip)   # 
    else:
        firewall.drop_ip4(ip)

    #add db thingy that updates the user as "droped"
    data.DbActiveIp4(ip,0)
		


if __name__ == '__main__':
    main()
