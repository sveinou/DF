#/usr/bin/python

import sys
from df_auth import Auth

pwd_min_length = 4

def get_input():
	"""
	Gets username,password and IP-address from commandline
	and pases it on as dictionary.
	"""
	if(len(argv) != 4)
		raise ValueError("Not enough/Too many arguments")

	user = argv[1]
	password = argv[2]
	ip = argv[3]
	if(type(user) != str)	
		raise ValueError("User not string!")
	elif(type(password) != str or len(password) < pwd_min_length)
		raise ValueError("Input error on password")
	elif(type(ip) != str or len(ip) < 7)
		raise ValueError("error on IP input")

	return {'username':user, 'password': password, 'ip_addr':ip}

def main():
	inputs = get_input()
	
	Auth.set_user(input['username'])
	Auth.set_password(input['password'])
	if(!Auth.login())
		raise ValueError("Login failes")

	#Code contiunes...
	


if __name__ == '__main__':
	main()
