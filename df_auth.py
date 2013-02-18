class auth:
	""" Does check of user and password to system """
	
	import pam
	import sys
	
	def __init__(self):
		self.logininfo = get_vars()

	def set_user(user):
		"""Checks user, sets variable"""
		if(str != "" and type(user) == str):
			self.user = user

	def set_password(password):
		"""Checks password, sets variable"""
		if(str != "" and type(user) == str):
			self.user = user

	def login():
		"""Does actual login-challange to \"login\"-program."""
		return pam.authenticate(user,password)
