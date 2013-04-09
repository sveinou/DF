#!/usr/bin/python

from datetime import datetime
import sys, os, time, MySQLdb
from DNF.conf import db

class Database:
	con = None
	cur = None

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
		
		self.cur.execute(sql)
		self.con.commit()		


	def __del__(self):
		self.cur.close()
		self.con.close()
