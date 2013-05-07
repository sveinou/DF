#!/usr/bin/python

import subprocess
from time import time
from DNF.conf import bandwidth as bw
from DNF.stats.df_user_stats import Statistics as stats
from DNF.gui import Gui

class Con:

	#returns latency in ms
	def get_ping(self,address):

		ms = 0.0
		p = subprocess.Popen(["ping","-c", "4", address], stdout = subprocess.PIPE)
		for word in p.communicate()[0].split(' '):
			if "time" in word and "=" in word:
				ms += float(word.split("=")[1])
		return ms/4

	def ping_cal(self,address):
		ms = 0.0
		times = 100
		for i in range(times):
			Gui().loadingbar(i,"latency test")
			p = subprocess.Popen(["ping","-c", "1", address], stdout = subprocess.PIPE)
			for word in p.communicate()[0].split(' '):
				if "time" in word and "=" in word:
					ms += float(word.split("=")[1])
		Gui().loadingbar(100,"finished! ")
		return ms/times

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
			
	def find_if(self):
    		command = "/sbin/ifconfig | grep HWaddr | awk '{print $1;}'"
    		interfaces = subprocess.check_output(command, shell=True).split("\n")
    		internal=""
    		external=""
    		for interface in interfaces:
			x = int(interfaces.index(interface))+1
			x = int(100/len(interfaces)*x)
			Gui().loadingbar(x)

        		if interface:
                		command = "/bin/ping -c 1 -I %s 8.8.8.8 | grep 64" % interface
                		try:
                        		ping = subprocess.check_output(command, shell=True)
                        		if ping:
                                		external = interface
					else:
						internal = interface

                		except Exception, e:
                        		internal = interface
		Gui().loadingbar(100)
    		return{'ext':external,'int':internal}


		

