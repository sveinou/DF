#!/usr/bin/python

from time import sleep
import sys
import subprocess
import DNF.conf
import os
from sys import stdout
class Gui:

    def __init__(self):
  	if DNF.conf.verbose == 0:
		#f = open(os.devnull, "w")
		#sys.stdout = f
	

    def loadingbar(self, x, text="Loading"):
	num = 100
     	colorCode = 43
	if x == num: colorCode = 42
	print '\r%s: [\r%s: [\033[1;%dm%s\033[1;m%s] %d%%' %(text,text,colorCode, " "*(x/2), " "*(num/2-x/2), x),
	sys.stdout.flush()
	if x == num: print " "
    	return


    def __del__(self):
	#sys.stdout = open('/dev/tty', 'w')


