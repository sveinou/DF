#!/usr/bin/python

from DNF.database.storage import Database

import subprocess as sp


print "Welcome to DF Firewall 0.0001 Alpha"

print "Enter internal interface"
#internal_if = raw_input()
internal_if ="eth1"
print "Enter internal IP"
#my_ip = raw_input()
my_ip = "10.0.0.1"
print "Enter external interface"
#external_if = raw_input()
external_if = "eth0"
print "Use nat? (YES/NO)"
#nat = raw_input()
nat = "YES"




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
        "iptables -N ALLOWED",
        "iptables -N CONNLIMIT",
	"iptables -N TXLIMIT",
	"iptables -N RXLIMIT",
        "iptables -N LIMITED",
        "iptables -t nat -N ALLOWED",
        "iptables -A FORWARD -p udp -m multiport --ports 53 -j ACCEPT",
        "iptables -A FORWARD -j LIMITED",
        "iptables -A FORWARD -j ALLOWED",
        "iptables -t nat -A PREROUTING -j ALLOWED",
        "iptables -A POSTROUTING -t nat -o "+external_if+" -j MASQUERADE",
        "iptables -t nat -A PREROUTING -p tcp -m multiport --ports 80,443 -j DNAT --to-destination "+my_ip+":80",
        "iptables -A FORWARD -d "+my_ip+" -p tcp -m multiport --ports 80,443 -j ACCEPT",
        "iptables -A FORWARD -j DROP",
	"iptables -A CONNLIMIT -m connlimit --connlimit-above 50 -j REJECT",
	"iptables -A TXLIMIT -j MARK --set-mark 200",
	"iptables -A RXLIMIT -j MARK --set-mark 100",
        "iptables -I INPUT -p tcp --dport 22 -j ACCEPT"]

dhcp = "service isc-dhcp-server restart"

## Database drop / create tables

sql = "DROP table clients"
Database().alter(sql)
sql = "DROP table stats"
Database().alter(sql)
sql = "CREATE table clients (User varchar(80), Mac varchar(80), IP4 varchar(80), IP6 varchar(80), active int)"
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
		print rule
	elif nat == "YES" or nat == "yes":
		sp.call(rule, shell=True)
		print "NAT"
	else:
		pass

	
print "You should be good to go naow."
