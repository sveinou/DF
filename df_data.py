#/usr/bin/python

import sys
import sqlite3
import conf
import os


class Data:
	def connDB(self, sql):


		if not os.path.isfile('df.db'):
			tabl = """ 
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
			cur.execute(tabl)
			db.commit()
		else:
			db = sqlite3.connect('df.db')
			cur = db.cursor()

		if sql.startswith("select"):
			cur.execute(sql)
			return cur.fetchone()
		else:
			cur.execute(sql)
			db.commit()
		
		cur.close()
		db.close()

		return 
	


	def getRow(self,user):

		#returns the row of the user
		sql = "select * from clients where User='%s'" % user
		return Data().connDB(sql)

	


	def DbAddRow(self,user,mac,ip4,ip6):

		#add a new user, or updating an exsiting one


		if len(mac) != 17 and len(ip4) < 7 and len(ip4) > 17:
			raise ValueError("somthing od with ip4/mac")
		elif Data().getRow(user):
			sql = "UPDATE clients set Mac='%s', IP4='%s', IP6='%s', Active=1 WHERE User='%s'" % (mac,ip4,ip6,user) 
		else:
			sql = "INSERT INTO clients VALUES ('%s', '%s', '%s', '%s', 1) " % (user,mac,ip4,ip6)
		Data().connDB(sql)

	def DbActive(self,user,active):

	#acitvates or deactivates an user


		sql = "UPDATE clients SET Active=%s WHERE User='%s'" % (active,user)
	
		Data().connDB(sql)


	def DbUpdateRow(self,user,data):

	#updates one part in a user`s row

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

		Data().connDB(sql)
	



	
	


	

