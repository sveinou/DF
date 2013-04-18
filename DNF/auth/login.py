#!/usr/bin/python

import os,sys, subprocess
from DNF import conf
from DNF.auth.df_auth import Auth
from DNF.firewall.firewall import Firewall
from DNF.stats.info import Dhcp
from DNF.database.df_data import Data
from DNF.stats.logger import Log

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
        dhcp = Dhcp()    
        auth = Auth(indata['username'],indata['password'])
        firewall = Firewall()
        mac = dhcp.find_mac(indata['ip_addr'])
        data = Data()
        
        if not os.getuid() == 0:
            cmd = 'sudo /usr/local/bin/dynfw login %s %s %s' % (ip, username, password)
            return subprocess.call(cmd, shell=True) == 0
            
        if mac == False:
            # ip/mac pair does not exist in leasefile
            print "FEIL Mac/IP combo"
            return False
#            exit(conf.exit_status.ip_mac_mismatch_error)
        elif auth.login() != True:
            print "Login failed."
            log.info("LOGIN FAILED: "+indata['username']+" at "+ indata['ip_addr'])
            return False
#            exit(conf.exit_status.login_error)
        else:
            firewall.accept_ip4(indata['ip_addr'])

        ## DATABASE GOES HERE
        log.info("LOGIN OK: "+indata['username']+" at "+ indata['ip_addr'])
        data.DbAddRow(indata['username'],mac,indata['ip_addr'],"IPv6")
#	    print lease[1]+" "+lease[0]
        ### WRITE SOMETHING TO A LOGFILE? (this goes to stdout)
        print "Login successful, {0} at ip {1}".format(indata['username'], indata['ip_addr'])        
        return True
        
    def cli_login():
        log = Log(conf.files.loginlog)
        indata = self.check_input(username, password, ip)
        dhcp = Dhcp()    
        auth = Auth(indata['username'],indata['password'])
        firewall = Firewall()
        mac = dhcp.find_mac(indata['ip_addr'])
        data = Data()

        if mac == False:
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
        data.DbAddRow(indata['username'],mac,indata['ip_addr'],"IPv6")
#        print lease[1]+" "+lease[0]
        ### WRITE SOMETHING TO A LOGFILE? (this goes to stdout)
        print "Login successful, {0} at ip {1}".format(indata['username'], indata['ip_addr'])        
        return True
        exit(0)
        
if __name__ == '__main__':
    l = Login()
    if(os.getuid() == 0):
        l.cli_login(sys.argv[1],sys.argv[2], sys.argv[3])
    else:
        print "You must be root to get pam access."
