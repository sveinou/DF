#!/bin/bash

EXT=$3
INT=$2
IP=$1

# INSTALL DNF-package
echo -e "IP: $1 \nINTERNAL IF: $2 \nEXTERNAL IF: $3"
echo -e "Installing DNF python package"
pip uninstall DynamicNetworkFirewall
pip install dist/DynamicNetworkFirewall-0.3.dev1.tar.gz

# database config, create the needed tables
echo -e "setting up mySQL.."
mysql -u root -p -h localhost df < database.sql

# network options. interfaces, network mask, internal ip, package forwarding
/sbin/ifconfig $INT $IP netmask 255.255.255.0
echo 1 > /proc/sys/net/ipv4/ip_forward
service isc-dhcp-server restart

# firewall settings, nat or not, redirect, allow dns, drop rest,
iptables -F
iptables -t nat -F
iptables -N ALLOWED
iptables -N CONNLIMIT
iptables -N TXLIMIT
iptables -N RXLIMIT
iptables -N TXLIMIT
iptables -N RXLIMIT
iptables -N LIMITED
iptables -t nat -N ALLOWED
iptables -A FORWARD -p udp -m multiport --ports 53 -j ACCEPT
iptables -A FORWARD -j LIMITED
iptables -A FORWARD -j ALLOWED
iptables -t nat -A PREROUTING -j ALLOWED
iptables -A POSTROUTING -t nat -o $EXT -j MASQUERADE
iptables -t nat -A PREROUTING -p tcp -m multiport --ports 80,443 -j DNAT --to-destination $IP:80
iptables -A FORWARD -d $IP -p tcp -m multiport --ports 80,443 -j ACCEPT
iptables -A FORWARD -j DROP
iptables -A CONNLIMIT -m connlimit --connlimit-above 50 -j REJECT
iptables -A TXLIMIT -j MARK --set-mark 200
iptables -A RXLIMIT -j MARK --set-mark 100
iptables -A CONNLIMIT -m connlimit --connlimit-above 50 -j REJECT
iptables -A TXLIMIT -j MARK --set-mark 200
iptables -A RXLIMIT -j MARK --set-mark 100
iptables -I INPUT -p tcp --dport 22 -j ACCEPT
