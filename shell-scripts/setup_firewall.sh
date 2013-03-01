#/bin/bash
## $1 = IP, $2 = Internal if, $3 = external if

ip="/sbin/iptables"

/sbin/ifconfig $2 $1 netmask 255.255.255.0
service isc-dhcp-server restart

#tillater forwarding av ipv4
echo 1 > /proc/sys/net/ipv4/ip_forward

#flusler old rules
$ip -F
$ip -t nat -F

#1 til alle nat
$ip -A  POSTROUTING -t nat -o $3 -j MASQUERADE

#redirekter all trafikk til gjitt ip
$ip -t nat -A PREROUTING -p tcp -m multiport --ports 80,443 -j DNAT --to-destination $1:80


#forward regler, dropper alt utenom 80 og 443:
$ip -I FORWARD -d $1 -p tcp -m multiport --ports 80,443 -j ACCEPT
$ip -I FORWARD -p udp -m multiport --ports 53 -j ACCEPT
$ip -A FORWARD -j DROP


#alltid kjekt med ssh
$ip -I INPUT -p tcp --dport 22 -j ACCEPT


$ip -L
    $ip -t nat -L
