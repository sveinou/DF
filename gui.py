#!/usr/bin/python

from time import sleep
import sys
import subprocess
import DNF.conf
import os
class Gui:

    def __init__(self):
  if DNF.conf.verbose == 0:
		f = open(os.devnull, "w")
		sys.stdout = f
	

    def loadingbar(self, x, text=""):
	num = 100
     	colorCode = 43
	if x == num: colorCode = 42
	print '\rLoading: [\rLoading: [\033[1;%dm%s\033[1;m%s] %d%%. %s       ' %(colorCode, " "*(x/2), " "*(num/2-x/2), x, str(text)),
	sys.stdout.flush()
    
    	return

    def welcome(self):
	subprocess.call('clear', shell=True)
	print "\n\n\n\n \033[92m"
	print " ___________________________"
	print "|                           |"
	print "|      dynfw installer      |"
	print "|                           |"
	print "|___________________________|"
	print "\033[0m \n\n"
	



    def question(self, text):
	colorCode = 92
	print "\r " +" "*100,
	print "\r \033[%dm---- %s ----\033[0m: " %(colorCode, text),
	answer = raw_input(),

	return answer


	

    def message(self, text):
	colorCode = 91 # red
	print "\r \033[%dm---- %s ----\033[0m" %(colorCode, text)
 



    def __del__(self):
	sys.stdout = open('/dev/tty', 'w')
