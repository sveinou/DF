#!/usr/bin/python

import subprocess
from time import time

class Con:
	
	#returns latency in ms
	def get_ping(self,address):
		
		ms = 0.0
		p = subprocess.Popen(["ping","-c", "4", address], stdout = subprocess.PIPE)
		for word in p.communicate()[0].split(' '):
			if "time" in word and "=" in word:
				ms += float(word.split("=")[1])
		return ms/4

	#returns how long it takes to download given file
	def download_time(self,address):
		
		first = time()
		fh = open("NUL","w")
		subprocess.call(["wget",address],stdout = fh, stderr = fh)
		fh.close()
		after = time()
		return after - first	

	


#print Con().get_ping("vg.no")

	#7.1 MB file from uninett (fast server)
#print Con().download_time("ftp://ftp.uninett.no/debian/ls-lR.gz")
