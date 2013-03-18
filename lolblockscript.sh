#!/bin/bash

iptables -t nat -A PREROUTING -p tcp -m multiport --ports 80,443 -j DNAT --to-destination 158.38.185.1:8080
iptables -A FORWARD -P DROP
iptables -A FORWARD -p tcp -m multiport --ports 80,443 -j ACCEPT
iptables -A FORWARD -p udp -m multiport --ports 80,443 -j ACCEPT
