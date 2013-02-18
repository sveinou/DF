#/usr/bin/python
import subprocess
import sys

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

def drop_ip4(ip):

	rules = ["/sbin/iptables -D FORWARD -d"+ip+" -j ACCEPT",
		"/sbin/iptables -D FORWARD -s"+ip+" -j ACCEPT",
              	"/sbin/iptables -t nat -D PREROUTING -d"+ip+" -j ACCEPT",
              	"/sbin/iptables -t nat -D PREROUTING -s"+ip+" -j ACCEPT",]
	
	for rule in rules:
		subprocess.call(rule, shell=True)



def drop_ip6(ip):
	rules = ["/sbin/ip6tables -D FORWARD -d"+ip+" -j ACCEPT",
		"/sbin/ip6tables -D FORWARD -s"+ip+" -j ACCEPT",]
	

	for rule in rules:
	 subprocess.call(rule, shell=True)	


def main():
	input = get_input()
	ip = input['ip_addr']

	if len(ip) > 15:
		drop_ip6(ip)
 	else:
		drop_ip4(ip)

	#add db thingy that updates the user as "droped"


if __name__ == '__main__':
	main()
