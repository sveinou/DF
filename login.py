#!/usr/bin/python

import sys
import subprocess
import conf
from df_auth import Auth
from df_firewall import Firewall
from df_findip import DHCP
from df_data import Data
from logger import Log

class Login():
    def check_input(self,user,password,ip):

        if type(user) != str:	
            raise ValueError("User not string!")
        elif type(password) != str:
            raise ValueError("Input error on password")
        elif type(ip) != str or len(ip) < 7:
            raise ValueError("error on IP input")

        return {'username':user, 'password': password, 'ip_addr':ip}


    def ip4(self,username, password, ip):
		
        log = Log(conf.files.loginlog)
        indata = self.check_input(username, password, ip)
            
        auth = Auth(indata['username'],indata['password'])
        firewall = Firewall()
        dhcp = DHCP(None)   ## Uses default leasefile given in conf.py
        lease = 1 #dhcp.get_ipv4_lease(indata['ip_addr']);
        data = Data()

        if lease == None:
            # ip/mac pair does not exist in leasefile
    	    print "FEIL Mac/IP combo"
            exit(conf.exit_status.ip_mac_mismatch_error)
        elif auth.login() != True:
            print "Login failed."
            log.info("LOGIN FAILED: "+indata['username']+" at "+ indata['ip_addr'])
            exit(conf.exit_status.login_error)
        else:
            firewall.accept_ip4(indata['ip_addr'])

	    ## DATABASE GOES HERE
        log.info("LOGIN OK: "+indata['username']+" at "+ indata['ip_addr'])
        data.DbAddRow(indata['username'],"na",indata['ip_addr'],"IPv6")
#	    print lease[1]+" "+lease[0]
        ### WRITE SOMETHING TO A LOGFILE? (this goes to stdout)
        print "Login successful, {0} at ip {1}".format(indata['username'], indata['ip_addr'])
        
        return
