import conf
import re
from df_data import Data 
from df_findip import DHCP
def get_input():
    """
        Gets username,password and IP-address from commandline
        and pases it on as dictionary.
    """
    if len(sys.argv) != 2:
        raise ValueError("Not enough/Too many arguments")

	ip = sys.argv[1]

	ipcheck = re.compile(conf.filter.ipv4_exact)
	
    if type(ip) != str:
        raise ValueError("User not string!")
    elif ipcheck.match(ip) == None:
        raise ValueError("Not IPv4 addr")
    else:
        return {'ipv4_addr':ip}


	
def check_user(ip):
    return Data().isActiveIp44(ip) and DHCP(None).ip_exists(ip)

def main():
    indata = get_input()
	
    if checkuser(indata['ipv4_addr']):
        print("ACTIVE")
        exit(conf.exit_status.user_already_logged_in)
	

if __name__ == '__main__':
    main()
