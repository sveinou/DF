#!/usr/bin/python
import subprocess
import os
import sys
import time

def missing(packages):
        """
        returns the packgages that are missing
        """
        missing = ""
        for package in packages.split():
                try:
                        DEVNULL = open(os.devnull, 'w')
                        dpkg = subprocess.Popen(["dpkg","-s",package], stdout = subprocess.PIPE, stderr = DEVNULL)
                        out = dpkg.communicate()[0]
                        if not "Status: install " in out:
                                missing += package+" "
                except Exception, e:
                        error_log(e)
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
	subprocess.call("cd /opt/DF; /usr/bin/python ./setup.py install", shell=True)		
	logpath = r'/var/log/dnf/'
	default = "/var/log/dnf/collect.log"
	webservice = "/var/log/dnf/django.log"
	access  = "/var/log/dnf/access.log"
	if not os.path.exists(logpath): os.makedirs(logpath)
	if not os.path.exists("/var/run/dynfwd"): os.makedirs("/var/run/dynfwd")
	subprocess.call("touch "+default, shell=True)
	subprocess.call("touch "+webservice, shell=True)
	subprocess.call("touch "+access, shell=True)
	
def change_config(search,replace,file_path):
	
	with open(file_path, 'r') as file: data = file.readlines()
	for line in data:
		if search in line:
			data[data.index(line)] = replace+"\n"
	with open(file_path, 'w') as file: file.writelines(data)
	return

def chmod_file(file, mode):
	cmd = 'chmod %s %s' % (mode, file)
	subprocess.call(cmd, shell=True)
	

def network_iptables(IP4,mask,NAT):
	try:
		import DNF.conf as conf
		external = conf.external_interface
		internal = conf.internal_interface
	except ImportError, e:
        	message("ohLord! seams like there is somthing wrong with our code")
        	error_log(e)
        	sys.exit
	command = ("/bin/bash /opt/DF/iptables.sh %s %s %s %s %s") %(external,internal,IP4,mask,NAT)
	subprocess.call(command,shell=True)
	
def database():
	try:
		
		subprocess.call("mysql -u root -p -h localhost < /opt/DF/db.sql", shell=True)
	except Exception, e:
		message("Too hard, was it? Type in the root password for MYSQL server to make the DNF database")
		answ = question("exit ??(Y/N)"("Y","N"))
		if answ is "N":
			sys.exit
		else:
			database()
	
def intro():
	"""
	prints out an intro to the installation, dynamicly after the 
	column size of current shell. ish
	"""
	#meh, have to change stuffs
	columns = int(subprocess.Popen(["tput","cols"], stdout = subprocess.PIPE).communicate()[0])
	subprocess.call("clear", shell=True)
	colorcode = 32
	text1 = "Dynamic Network Firewall v.0.5.rc1\n Installation and setup"
	text2 = "by Svein Ove Undal"
	text3 = "and Espen Gjerde"
	warning = "WARNING, installation requires two ACTIVE NIC's and a working internet connection"
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
	columns = int(subprocess.Popen(["tput","cols"], stdout = subprocess.PIPE).communicate()[0])
	text = "%s%s" %(" "*int(columns/2-len(text)),text)
	print ""
	print ""
	try:
		ans = raw_input(text+":")
        except Exception, e:
                message("I think you might have forgotten that input i asked you about... ")

	if not answers: return ans	
	for answer in answers:
		if ans.upper() == answer:
			return answer
	question(tex,answers)


def message(text):

	subprocess.call("clear", shell=True)	
        colorcode = 35
        text = '\033[%dm%s\033[0m'%(colorcode,text)
        columns = int(subprocess.Popen(["tput","cols"], stdout = subprocess.PIPE).communicate()[0])
        text = "%s%s" %(" "*int(columns/2-len(text)),text)
        print ""
        print ""
	print text
	print ""
	print ""
	time.sleep(1)

packages = ("git apache2 mysql-server python-mysqldb isc-dhcp-server python-daemon python-django libapache2-mod-wsgi sudo")
#packagespath = ("/usr/bin/git","/usr/sbin/apache2","/usr/bin/mysql","/usr/lib/python2.7/dist-packages/MySQLdb/__init__.pyc","/usr/sbin/dhcpd","/usr/lib/pymodules/python2.7/daemon/__init__.pyc")
ping_server = "8.8.8.8"

intro()
answ = question("This will install and setup Dynamic Network Firewakk, move along? (Y/N)",('Y','N'))
if answ == 'N':
	sys.exit()
					# packageTestInstall
message("Nice choice. Checking dependencies... ")
miss = missing(packages)
if miss:
	message("There are some packages missing")
	answ == question("Install the missing packages?(Y/N)",("Y","N"))
	if answ == "N":
		sys.exit()
	elif answ == "Y":
		message("Installing some awesome packages")
		install(packages)
		message("And we're done installing!")
				
subprocess.call("a2dissite default", shell=True)
subprocess.call("/etc/init.d/apache2 reload", shell=True)

if missing(packages):
	message("Something went wrong. Please check your apt-settings. Exiting")
	sys.exit()
	
					#DYNDNF installation
message("Continuing to download and install the DNF-system")		
pull_create_install()
message("It probobly worked!")
					#adding database and user
message("setting up the database. You will now be asked to enter your root-password for your database.")	
database()

					#configChanges - interface
message("Now we are gonna set up the config file!")
message("Testing network interfaces ...")
try:
	from DNF.stats.con_status import Con
except ImportError, e:
	message("ohLord! seams like there is somthing wrong with our code!! more info in logfile")
	error_log(e)
	sys.exit()
interfaces = Con().find_if()
internal = interfaces['int']
external = interfaces['ext']
external_ip = Con().inferface_ip(external)
if not internal:
	message("Did not find a second interface. Did you rememer to activate it?")
	message("Anyways... im out.")
	sys.exit()
message("Internal interface "+internal+". External interface "+external)
answ = question("is this correct?(Y/N)",("Y","N"))
if answ == "N":
	message("Not? Too bad. Check your config and retry.") #im getting tired
	sys.exit()
elif answ == "Y":
	change_config("internal_interface","internal_interface = "+internal,"/etc/dnf/dnf.conf") 
	change_config("external_interface","external_interface = "+external,"/etc/dnf/dnf.conf")
	change_config("external_ip","external_ip = "+external_ip,"/etc/dnf/dnf.conf") 
	
					#configChanges - interface
					
message("Latency test next, please make sure there is nothing using your internetconnection")
question("Are you sure there is nothing taking up this connection?(YES)",("YES","Y"))
ms = Con().ping_cal(ping_server)
ms += 2
answ = "lol"
while answ is not "Y":
	answ = question("Set latency_high to "+str(ms)+"(Y/N)",('Y','N'))
	if answ == "N":
		message("So.. you have a better suggestion? Type it in!")
		ms = question("what latency_high setting you want then?(integer in ms)")
message("Awesome! Editing the freaking file")		
change_config("latency_high","latency_high = "+str(int(ms)),"/etc/dnf/dnf.conf")
change_config("latency_test_addr","latency_test_addr = "+ping_server,"/etc/dnf/dnf.conf")

					#configChanges - rxs/txs
message("We need to know how good your connection is.")
answ = "notY"
rx = "1000"
tx = "1000"
while answ is not "Y":
	rx = question("What is the rx(download) speed in K(BYTES)")
	tx = question("What is the tx(upload) speed in K(BYTES)")
	answ = question("is this correct? tx="+tx+"rx="+rx+" (Y/N)",("Y","N"))
message("FANTASTIC! We're soon done here :)")
change_config("max_rxs","max_rxs = "+rx,"/etc/dnf/dnf.conf")
change_config("max_txs", "max_txs = "+tx,"/etc/dnf/dnf.conf")


message("Firewall and network configuration")

change_config('INTERFACES=""','INTERFACES="'+internal+'"',"/etc/default/isc-dhcp-server")
IP4 = "10.0.0.1"
mask = "/24"
NAT = "Y"
message("Loginpage set to run at %s:8080" % (IP4))
change_config("internal_network","internal_network = "+IP4+mask,"/etc/dnf/dnf.conf")
change_config("NMV", "NameVirtualHost "+IP4+":8080","/etc/apache2/conf.d/djangoDNF.conf")
change_config("<VirtualHost *:80>","<VirtualHost "+IP4+":8080>", "/etc/apache2/conf.d/djangoDNF.conf")

subprocess.call("/bin/mv /etc/dhcp/dhcpd.conf /etc/dhcp/dhcpd.conf.old",shell=True)
subprocess.call("/bin/mv /etc/dhcp/dhcpd.dnf.conf /etc/dhcp/dhcpd.conf",shell=True)
message("Now running the firewall, interface and dhcp script")
answ = question("with your permission, this will flush iptables rules, and change internal ip. proceed?(Y/N)",("Y","N"))
if answ is not "Y":
	message("That's OK, You have to do it yourself THEN!... but don't come complaining to ME")
	sys.exit()
message("Doing some cleanup... ")

subprocess.call("a2dissite default", shell=True)
subprocess.call("/etc/init.d/apache2 reload", shell=True)

chmod_file('/etc/sudoers.d/DNFsudorights', '440')

network_iptables(IP4,mask,NAT)
print("Configuration file: /etc/dnf/dnf.con")
print("You can now log in to the admin-interface. \nUsername: \"espen\" \nPassowrd \"espen\"")
print("Address should be http://%s:8080/" % (IP4))



	

#pidfolder, daemon log
