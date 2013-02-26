

import sys
import subprocess
from df_auth import Auth
from df_firewall import Firewall
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
    if len(sys.argv) != 4:
        raise ValueError("Not enough/Too many arguments")

    user = sys.argv[1]
    password = sys.argv[2]
    ip = sys.argv[3]
    if type(user) != str:	
        raise ValueError("User not string!")
    elif type(password) != str or len(password) < pwd_min_length:
        raise ValueError("Input error on password")
    elif type(ip) != str or len(ip) < 7:
        raise ValueError("error on IP input")

    return {'username':user, 'password': password, 'ip_addr':ip}


def main():
    indata = get_input()
	
    auth = Auth(indata['username'],indata['password'])
    firewall = Firewall()

    if auth.login() != True:
        raise ValueError("Login failes")
    else:
        firewall.accept_ip4(indata['ip_addr'])


if __name__ == '__main__':
	main()
