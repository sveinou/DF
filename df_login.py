#/usr/bin/python

import sys
import subprocess
from df_auth import Auth

"""	df_login.py username password ip_address
	Tries to login username with password. If successful, it will unblock 
	the ip-address from iptables. 

"""


pwd_min_length = 4

def get_input():
	"""
	Gets username,password and IP-address from commandline
	and pases it on as dictionary.
	"""
	if len(argv) != 4:
		raise ValueError("Not enough/Too many arguments")

	user = argv[1]
	password = argv[2]
	ip = argv[3]
	if type(user) != str:	
		raise ValueError("User not string!")
	elif type(password) != str or len(password) < pwd_min_length:
		raise ValueError("Input error on password")
	elif type(ip) != str or len(ip) < 7:
		raise ValueError("error on IP input")

	return {'username':user, 'password': password, 'ip_addr':ip}


def accept_ip4(ip):

 	rules = ["/sbin/iptables -I FORWARD -d"+ip+" -j ACCEPT",
		"/sbin/iptables -I FORWARD -s"+ip+" -j ACCEPT",
              	"/sbin/iptables -t nat -I PREROUTING -d"+ip+" -j ACCEPT",
                "/sbin/iptables -t nat -I PREROUTING -s"+ip+" -j ACCEPT",]
 
	for rule in rules:
  		subprocess.call(rule, shell=True)

def accept_ip6(ip):

        rules = ["/sbin/iptables -I FORWARD -d"+ip+" -j ACCEPT",
                "/sbin/iptables -I FORWARD -s"+ip+" -j ACCEPT",]
 
        for rule in rules:
                subprocess.call(rule, shell=True)

def main():
	inputs = get_input()
	
	auth = Auth(inputs['username'],inputs['password'])
	if auth.login() != True:
		raise ValueError("Login failes")
	else:
		accept_ip4(input['ip_addr'])


if __name__ == '__main__':
	main()
