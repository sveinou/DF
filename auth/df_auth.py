import pam

class Auth:
	""" Does check of user and password to system """
#	user = None
#	password = None	

#	def __init__(self):
#		self.username = None
#		self.password = None

	def __init__(self, username, password):
		self.username = username
		self.password = password

	def set_user(self,username):
		"""Checks user, sets variable"""
		if(user != "" and type(username) == str):
			self.username = username

	def set_password(self,password):
		"""Checks password, sets variable"""
		if(password != "" and type(password) == str):
			self.password = password

	def login(self):
		"""Does actual login-challange to \"login\"-program."""
		return pam.authenticate(self.username,self.password)
