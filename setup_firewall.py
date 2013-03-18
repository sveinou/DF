#!/usr/bin/python

import subprocess as sp

print "Welcome to DF Firewall 0.0001 Alpha"

print "Enter internal interface"
internal_if = raw_input()

print "Enter internal IP"
my_ip = raw_input()

print "Enter external interface"
external_if = raw_input()

print "\n\nis this your settings?"
print "External Interface: "+external_if
print "Internal Interface: "+internal_if
print "IP internal if: "+my_ip
print "\nEnter YES to continue"

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

print "Enabling IPv4 Routing...."
sp.call(routing, shell=True)
print "Setting up interface..."
sp.call(interface, shell=True)
print "Restarting DHCP-server"
sp.call(dhcp, shell=True)
print "Setting up iptables..."
for rule in fw_rules:
	sp.call(rule, shell=True)

print "You should be good to go naow."
