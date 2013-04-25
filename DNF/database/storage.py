#!/usr/bin/python

from datetime import datetime
import sys, os, time, MySQLdb
from DNF.conf import db

class Database:
	con = None
	cur = None
	"""
	This is the only class that connects to the database
	the init method will create the connection and the cursor
	the del method is an outro method, that will close the connection
	"""
	def __init__(self):
		
		server = db.server
		user = db.user
		password = db.pw
		name = db.name
		self.con = MySQLdb.connect(server,user,password,name)	
		self.cur = self.con.cursor()
	
	def get_row(self,sql):
		self.cur.execute(sql)
		return self.cur.fetchone()

	def get_all_rows(self,sql):
		self.cur.execute(sql)
		return self.cur.fetchall()

	def alter(self,sql):
		a = self.cur.execute(sql)
		b = self.con.commit()
		print("exec = %s , commit = %s" %(str(a), str(b)))		


	def __del__(self):
		self.cur.close()
		self.con.close()
