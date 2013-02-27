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
		
		sql = "UPDATE clients SET Mac='%s', IP4='%s', IP6='%s', Active=TRUE WHERE User='%s'" % (mac,ip4,ip6,user)
		cur.execute(sql)
		return True	

	else:
		sql = "INSERT INTO clients VALUES ('%s', '%s', '%s', '%s', TRUE) " % (user,mac,ip4,ip6)
		cur.execute(sql) 
		db.commit
		
		cur.execute("select * from clients ")
		for row in cur.fetchall():
			print row[0]

		return True



	
	


db("neidu","loolmac","ip4","ip6")
	

