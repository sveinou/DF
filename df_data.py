#/usr/bin/python

import sys
import sqlite3
import conf
import os

"""
USAGE: 
no args, it prints the database
one arg, the user. it prints that users row
two args, user data(ip4,mac,ip6) it wil update what you type in
two args, user drop, it vil set the active flag as null
4 args, it wil create a compleet new row with active status
4 args, and user already exists. updates and activate that user.


"""

def connDB():

	if not os.path.isfile('df.db'):
		sql = """ 
		CREATE TABLE clients
		(
		User text,
		Mac text,
		IP4 text,
		IP6 text,
		Active integer
		 )
		"""
		db = sqlite3.connect('df.db')
		cur = db.cursor()
		cur.execute(sql)
		db.commit()
	else:
		db = sqlite3.connect('df.db')
		cur = db.cursor()

	return {'db':db,'cur':cur}

def closeDB(db,cur):
	cur.close()
	db.close()

def executeDB(sql):
        conn = connDB()
        db = conn['db']
        cur = conn['cur']
        cur.execute(sql)
        db.commit()
        closeDB(db,cur)
	

def printDB():

	conn = connDB()
	cur = conn['cur']
	db = conn['db']

	cur.execute("select * from clients")
	rows = cur.fetchall()
	for row in rows:
		print ("%s %s %s %s %i") % (row[0],row[1],row[2],row[3],row[4])
	
	closeDB(db,cur)

def printRow(user):
	conn = connDB()
        cur = conn['cur']
        db = conn['db']
	sql = "select * from clients where User='%s'" % user
        cur.execute(sql)
        row = cur.fetchone()

        closeDB(db,cur)
	return row

	


def DbAddRow(user,mac,ip4,ip6):

	if len(mac) != 17 and len(ip4) < 7 and len(ip4) > 17 and ip6 < 17:
		raise ValueError("somthing od with ip4/mac/ip6")
	elif printRow(user):
		sql = "UPDATE clients set Mac='%s', IP4='%s', IP6='%s', Active=1 WHERE User='%s'" % (mac,ip4,ip6,user) 
	else:
		sql = "INSERT INTO clients VALUES ('%s', '%s', '%s', '%s', 1) " % (user,mac,ip4,ip6)

	executeDB(sql)

def DbActive(user,active):
	

	sql = "UPDATE clients SET Active=%s WHERE User='%s'" % (active,user)
	
	executeDB(sql)


def DbUpdateRow(user,data):

 		# maybeh make a better check for it...


	if len(data) > 17:
       		type = "IP6"
  	elif len(data) == 17:
       		type = "Mac"
        elif len(data) > 7:
               	type = "IP4"
	else:
		raise ValueError("input error")

	sql = "UPDATE clients SET %s='%s', Active=1 WHERE User='%s'" % (type,data,user)



	excuteDB(sql)
	



#			sql = "UPDATE clients SET Mac='%s', IP4='%s', IP6='%s', Active=TRUE WHERE User='%s'" % (mac,ip4,ip6,user)






def main():
	argv = sys.argv

	if len(argv) == 3:
		user = argv[1]
		data = argv[2]
		if data == "1" or data == "0":
			DbActive(user,data)
		else:
			DbUpdateRow(user,data)


	elif len(argv) == 4:
                user = argv[1]
                mac = argv[2]
                ip4 = argv[3]
		ip6 = "NA"
		DbAddRow(user,mac,ip4,ip6)

	elif len(argv) == 5:
                user = argv[1]
                mac = argv[2]
                ip4 = argv[3]
                ip6 = argv[4]
                DbAddRow(user,mac,ip4,ip6)
		
	elif len(argv) == 2:
		user = argv[1]
		row =printRow(user)
		print ("%s %s %s %s %i") % (row[0],row[1],row[2],row[3],row[4])


	elif len(argv) == 1:
		printDB()

	else:
		raise ValueError(" to manny args ")
		

	



if __name__ == '__main__':
	main()

	
	


	

