#!/bin/bash

ip=$1
#mac=$2
logfile=/var/log/expired_ips
dropscript=/var/www/git/DF/df_drop.py


echo -e "EXPIRED: $ip at mac" >> $logfile 

/usr/bin/python $dropscript $ip
