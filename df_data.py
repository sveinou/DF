#/usr/bin/python

import sys
import MySQLdb
import conf

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
		if len(argv) == 5:
			ip6 = argv[4]
		else:
			ip6 = "NA"

		if  len(ip4) < 7:
			raise ValueError("error on IP4 input")
		elif  len(mac) != 17:
			print len(mac)
 			raise ValueError("error on mac input")
		#elif type(ip6) != str or len(ip6) < 17:
		#	raise ValueError("error on ip6 input")
		return {'username':user, 'ip4_addr':ip4, 'mac_addr':mac, 'ip6_addr':ip6}

def get_input2():

	argv = sys.argv
	if len(argv) == 3:
		
		findUser = argv[1]
		data = argv[2]
		if len(data) > 17:
			type = "IP6"
		elif len(data) == 17:
			type = "Mac"
		elif len(data) > 7:
			type = "IP4" 
		else:
			raise ValueError("seccond var is nether an ip4, mac nor ip6")
		return {'User':findUser, 'data':data, 'type':type}

	else:
		raise ValueError(" this script needs atleast 2 args")
	
		return


def db(user,mac,ip4,ip6):

	"""
		
	this method adds a new entery to an exsisting db, or updates a line

	"""



	db = MySQLdb.connect(conf.db.server, conf.db.user, conf.db.pw, conf.db.name)
	cur = db.cursor()
	cur.execute("select * from clients WHERE User = %s", user)
	row = cur.fetchone()
	
	if row and row[4] == True :
		raise ValueError("User is actually Active") #perhaps some other errorThingy
		return False

	elif row and row[4] == False :
		
		if len(ip4) == 3:
			type = ip4
			data = mac
			sql = "UPDATE clients SET %s='%s', Active=TRUE WHERE User='%s'" % (type,data,user)
		
		else:
			sql = "UPDATE clients SET Mac='%s', IP4='%s', IP6='%s', Active=TRUE WHERE User='%s'" % (mac,ip4,ip6,user)
		cur.execute(sql)
		cur.execute("select * from clients ")
		return True	

	elif row and len(ip4) != 3:
		sql = "INSERT INTO clients VALUES ('%s', '%s', '%s', '%s', TRUE) " % (user,mac,ip4,ip6)
		cur.execute(sql) 
		db.commit
		return True

def main():
    	indata = get_input()
	indata2 = get_input2()
	
	if indata2['data']:		
    		d = db(indata2['User'],indata2['data'],indata2['type'],"NA")
    	elif indata['ip4_addr']:
		d = db(indata['User'],indata['mac'],indata['ip4'],indata['ip6'])
	print d


if __name__ == '__main__':
	main()

	
	


	

