#!/bin/bash

EXT = $1
IP = $2
NAT = $3

rules(){
iptables -F
iptables -t nat -F
iptables -N ALLOWED
iptables -N CONNLIMIT
iptables -N CUSTOM_FORWARD
iptables -N CUSTOM_INPUT
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
iptables -I FORWARD -j CUSTOM_FORWARD
iptables -I INPUT -j CUSTOM_INPUT
}

nat(){
iptables -A POSTROUTING -t nat -o $EXT -j MASQUERADE
}

