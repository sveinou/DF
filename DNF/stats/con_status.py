#!/usr/bin/python

import subprocess
from time import time
from DNF import conf
from DNF.stats.df_user_stats import Statistics as stats

class Con:
	bw = conf.bandwidth

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
		time = self.download_time(self, self.bw.download_file_addr)
		if time > self.bw.download_time_hig:
			return True
		else:
			return False

	def is_hig_latency(self):
		ms = self.download_time(self, self.bw.latency_test_addr)
		if ms > self.bw.latency_hig:
			return True
		else:
			return False

	def check(self):
		#if is_hig_latency || is_hig_ping
			#find top users (connections and download)
			limit
		return

		

