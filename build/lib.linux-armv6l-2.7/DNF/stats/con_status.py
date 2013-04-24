#!/usr/bin/python

import subprocess
from time import time
from DNF.conf import bandwidth as bw
from DNF.stats.df_user_stats import Statistics as stats

class Con:

	#returns latency in ms
	def get_ping(self,address):

		ms = 0.0
		p = subprocess.Popen(["ping","-c", "4", address], stdout = subprocess.PIPE)
		for word in p.communicate()[0].split(' '):
			if "time" in word and "=" in word:
				ms += float(word.split("=")[1])
		return ms/4

	#returns how long it takes to download given file in secs
	def download_time(self,address):
		filename = address.split('/')[-1]
		first = time()
		fh = open("NUL","w")
		subprocess.call(["wget",address],stdout = fh, stderr = fh)
		fh.close()
		after = time()
		subprocess.call("rm NUL " + filename,shell=True)
		return after - first	


	def is_slow(self):
		time = self.download_time(bw.download_file_addr)
		if time > bw.download_time_hig:
			return True
		else:
			return False

	def is_hig_latency(self):
		ms = self.get_ping(bw.latency_test_addr)
		if ms > bw.latency_hig:
			return True
		else:
			return False


		

