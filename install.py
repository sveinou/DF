#!/usr/bin/python
import subprocess
import os
import sys
import time
def missing(packages):
    """
    returns the packages that are missing
    """

    missing = ""
    for package in packages:
    	try:
		if "/" in package:
    			with open(package): pass
	except IOError:
   		missing += " "+package

    return missing

def install(packages):
	
	subprocess.call("apt-get install "+packages, shell=True)
	
def error_log(error):
	f = open("dnfErrors.log",'w')
	f.write(error)
	f.close

def pull_create_install():

	newpath = r'/opt/DF' 
	if not os.path.exists(newpath): os.makedirs(newpath)
	subprocess.call("cd /opt/DF; git init; git pull https://github.com/sveinou/DF.git", shell=True)
	subprocess.call("/usr/bin/python /opt/DF/setup.py install", shell=True)	

def change_config(search,replace):
	with open('/etc/dnf/dnf.conf', 'r') as file: data = file.readlines()
	for line in data:
		if search in line:
			data[data.index(line)] = replace+"\n"
	with open('/etc/dnf/dnf.conf', 'w') as file: file.writelines(data)
	return

def database():
	try:
		hmm = subprocess.check_output("mysql -u root -p -h localhost < /opt/DF/database.sql", shell=True)
	except Exception, e:
		message("you fucked up. type in the root password for MYSQL server to make the df database")
		database()
	
def intro():
	"""
	prints out an intro to the installation, dynamicly after the 
	column size of current shell. ish
	"""
	#meh, have to change stuffs
	columns = int(subprocess.check_output("tput cols", shell=True))
	subprocess.call("clear", shell=True)
	colorcode = 32
	text1 = "Dynfw setup"
	text2 = "by Svein Ove Undal"
	text3 = "and Espen Gjerde"
	warning = "WARNING, two networkcards and an active connection are needed to install"
	print "\033[%dm" %(colorcode)
	print " %s" %("_"*(columns/2+1))	
	print "|%s |" %(" "*(columns/2))	
	print "|%s |" %(" "*(columns/2))	
	print "|%s%s%s|" %((" "*(columns/4-len(text1)/2),text1," "*(columns/4-len(text1)/2)))	
	print "|%s |" %(" "*(columns/2))	
	print "|%s%s%s |" %((" "*(columns/4-len(text2)/2),text2," "*(columns/4-len(text2)/2)))	
	print "|%s%s%s |" %((" "*(columns/4-len(text3)/2),text3," "*(columns/4-len(text3)/2)))	
	print "|%s |" %(" "*(columns/2))	
	print "|%s|" %("_"*(columns/2+1))
	print "\033[0m"
	print ""
	print ""
        print "\033[31m%s%s\033[0m" %(" "*int(columns/2-len(warning)),warning)

	

def question(tex,answers=""):
	colorcode = 35
	text = '\033[%dm%s\033[0m'%(colorcode,tex)
	columns = int(subprocess.check_output("tput cols", shell=True))
	text = "%s%s" %(" "*int(columns/2-len(text)),text)
	print ""
	print ""
	ans = raw_input(text+":")
	if not answers: return ans	
	for answer in answers:
		if ans.upper() == answer:
			return answer
	question(tex,answers)


def message(text):

	subprocess.call("clear", shell=True)	
        colorcode = 35
        text = '\033[%dm%s\033[0m'%(colorcode,text)
        columns = int(subprocess.check_output("tput cols", shell=True))
        text = "%s%s" %(" "*int(columns/2-len(text)),text)
        print ""
        print ""
	print text
	print ""
	print ""
	time.sleep(1)

packages = ("git apache2 mysql-server python-mysqldb")
packagespath = ("/usr/bin/git","/usr/sbin/apache2","/usr/bin/mysql","/usr/lib/python2.7/dist-packages/MySQLdb/__init__.pyc")
ping_server = "8.8.8.8"

intro()
answ = question("This will install and setup the awesome dynfw, move allong?(Y/N)",('Y','N'))
if answ == 'N':
	sys.exit()
					# packageTestInstall
message("ofcourse you would! ")
miss = missing(packagespath)
if miss:
	message("There are some packages missing")
	answ == question("install the missing packages?(Y/N)",("Y","N"))
	if answ == "N":
		sys.exit()
	elif answ == "Y":
		message("installing some awesome packages")
		install(packages)
		message("installed hopfully some packages")
				

if missing(packagespath):
	message("meh, somthing wrong with packages, exiting")
	sys.exit()
	
					#DYNDNF installation
message("will now install dynfw")		
pull_create_install()
message("It probobly worked!")
					#adding database and user
message("setting up the database!, it will ask you for the root password")	
database()

					#configChanges - interface
message("Now we are gonna set up the config file!")
message("interface test")
try:
	from DNF.stats.con_status import Con
except ImportError, e:
	message("ohLord! seams like there is somthing wrong with our code!! more in logfile")
	error_log(e)
	sys.exit()
interfaces = Con().find_if()
internal = interfaces['int']
external = interfaces['ext']
if not internal:
	message("did not find a seccond interface, IM OUT!")
	sys.exit()
message("internal interface "+internal+". external interface "+external)
answ = question("is this correct?(Y/N)",("Y","N"))
if answ == "N":
	message("whell fuck you then!!") #im getting tired
	sys.exit()
elif answ == "Y":
	change_config("internal_interface","internal_interface = "+internal) 
	change_config("external_interface","external_interface = "+external)
	
					#configChanges - interface
					
message("latency test next, make sure there is nothing downloading")
question("Are you sure there is nothing taking up this connection?(YES)",("YES","Y"))
ms = Con().ping_cal(ping_server)
ms += 2
answ = "lol"
while answ is not "Y":
	answ = question("set latency_high to "+str(ms)+"(Y/N)",('Y','N'))
	if answ == "N":
		message("THEN YOU TYPE IT!!")
		ms = question("what latency_high setting you want then?(integer in ms)")
message("Awesome! editing the freaking file")		
change_config("latency_high","latency_high = "+str(int(ms)))
change_config("latency_test_addr","latency_test_addr = "+ping_server)

					#configChanges - rxs/txs
message("ok, we need to know how good your connection is")
answ = "notY"
rx = "1000"
tx = "1000"
while answ is not "Y":
	rx = question("what is the rx(download) speed in K(BYTES)")
	tx = question("what is the tx(upload) speed in K(BYTES)")
	answ = question("is this correct? tx="+tx+"rx="+rx+" (Y/N)",("Y","N"))
message("FANTASTIC soon done :) changing config")
change_config("max_rxs","max_rxs = "+rx)
change_config("max_txs", "max_txs = "+tx)

message("done for now!!")

#iptables
#ipaddress
#dhcpserver

	

