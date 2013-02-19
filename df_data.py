#/usr/bin/python

import sys

"""
This script takes an input, and are supposed to save it to somwhere, somthing
like an database. if it gets more than 3 variables it will create a new entery
if it gets two, it vil search up the user in the first arg, and save the 
seccond var where it belongs.

"""

def get_input():
	argv = sys.argv
	
	if len(argv) > 3:

		user = argv[1]
		ip4 = argv[2]
		mac = argv[3]
		#ip6 = argv[4]


		if  len(ip4) < 7:
			raise ValueError("error on IP4 input")
		elif  len(mac) != 17:
 			raise ValueError("error on mac input")
		#elif type(ip6) != str or len(ip6) < 17:
		#	raise ValueError("error on ip6 input")
		return {'username':user, 'ip4_addr':ip4, 'mac_addr':mac}


	elif len(argv) == 3:
		
		findUser = argv[1]
		data = argv[2]
		if len(data) > 17:
			type = "ip6"
		elif len(data) == 17:
			type = "mac"
		elif len(data) > 7:
			type = "ip4" 
		else:
			raise ValueError("seccond var is nether an ip4, mac nor ip6")
		return {'findUser':findUser, 'data':data, 'type':type}

	else:
		raise ValueError(" this scripts needs atleast 2 args")
		error = " lol "
	
		return
	
test = get_input()


print([str(item) for item in test])

