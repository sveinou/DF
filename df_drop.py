#/usr/bin/python
import subprocess
import sys
from df_firewall import Firewall

def get_input():
	"""
	Gets username and IP-address from commandline
	and pases it on as dictionary.
	"""
	argv = sys.argv
	if len(argv) != 3:
		raise ValueError("Not enough/Too many arguments")

	user = argv[1]
	ip = argv[2]
	if type(user) != str:	
		raise ValueError("User not string!")
	elif type(ip) != str or len(ip) < 7:
		raise ValueError("error on IP input")

	return {'username':user, 'ip_addr':ip}


def main():
	indata = get_input()
	ip = indata['ip_addr']
    firewall = Firewall()

	if len(ip) > 15:
		firewall.drop_ip6(ip)
 	else:
		firewall.drop_ip4(ip)

	#add db thingy that updates the user as "droped"


if __name__ == '__main__':
	main()
