#!/usr/bin/python

import subprocess
import DNF.conf as c

class limit:
	IF = c.external_interface

	def __init__(self):
	    pass

 	
        def activate_limit(self,tx,rx):
		limit().deactivate_limit()

                ## makes an rule that will limit packages with --set-mark 100(rx) or 200(tx) (from iptables)

                rules = ["/sbin/tc qdisc add dev "+self.IF+" root handle 1: htb default 30",
                        "/sbin/tc class add dev "+self.IF+" parent 1: classid 1:1 htb rate "+rx+" prio 1",
                        "/sbin/tc class add dev "+self.IF+" parent 1: classid 1:2 htb rate "+tx+" prio 1",
                        "/sbin/tc filter add dev "+self.IF+" parent 1:0 prio 1 protocol ip handle 100 fw flowid 1:1",
                        "/sbin/tc filter add dev "+self.IF+" parent 1:0 prio 1 protocol ip handle 200 fw flowid 1:2"]

                for rule in rules:
	                subprocess.call(rule, shell=True)


        def deactivate_limit(self):
                subprocess.call("/sbin/tc qdisc del dev "+self.IF+" root", shell=True)



#limit().deactivate_limit()  
#limit().activate_limit("1mbit","1mbit")

