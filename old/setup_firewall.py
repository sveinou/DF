#!/usr/bin/python

from database.storage import Database

import subprocess as sp

print "Welcome to DF Firewall 0.0001 Alpha"

print "Enter internal interface"
internal_if = raw_input()

print "Enter internal IP"
my_ip = raw_input()

print "Enter external interface"
external_if = raw_input()

print "Use nat? (YES/NO)"
nat = raw_input()





print "\n\nis this your settings?"
print "External Interface: "+external_if
print "Internal Interface: "+internal_if
print "IP internal if: "+my_ip
print "Use nat? "+nat 
print "\nEnter YES to continue"
print " OMG!! DATABASE WILL BE DROPED!!!"

resume = raw_input()
if resume != "YES":
	exit(0)

interface = "/sbin/ifconfig "+internal_if+" "+my_ip+" netmask 255.255.255.0"

routing = "echo 1 > /proc/sys/net/ipv4/ip_forward"

fw_rules = ["iptables -F",
	"iptables -t nat -F",
	"iptables -A POSTROUTING -t nat -o "+external_if+" -j MASQUERADE",
	"iptables -t nat -A PREROUTING -p tcp -m multiport --ports 80,443 -j DNAT --to-destination "+my_ip+":80",
	"iptables -I FORWARD -d "+my_ip+" -p tcp -m multiport --ports 80,443 -j ACCEPT",
	"iptables -I FORWARD -p udp -m multiport --ports 53 -j ACCEPT",
	"iptables -A FORWARD -j DROP",
	"iptables -I INPUT -p tcp --dport 22 -j ACCEPT"]

dhcp = "service isc-dhcp-server restart"

## Database drop / create tables

sql = "DROP table clients"
Database().alter(sql)
sql = "DROP table stats"
Database().alter(sql)
sql = "CREATE table clients (User varchar(80), Mac varchar(80), IP4 carchar(80), IP6 varchar(80), active int)"
Database().alter(sql)
sql = "CREATE table stats (User varchar(80), Connections bigint(255), tx_total bigint(255), rx_total bigint(255), txs bigint(255), rxs bigint(255), Time timestamp)"
Database().alter(sql)


print "Enabling IPv4 Routing...."
sp.call(routing, shell=True)
print "Setting up interface..."
sp.call(interface, shell=True)
print "Restarting DHCP-server"
sp.call(dhcp, shell=True)
print "Setting up iptables..."
for rule in fw_rules:
	if not "POSTROUTING" in rule:
		sp.call(rule, shell=True)
	elif nat = "YES":
		sp.call(rule, shell=True)
	else:
		pass

	
print "You should be good to go naow."
