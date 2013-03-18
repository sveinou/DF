#!/usr/bin/python

import sys, conf
from df_data import Data
from df_user_stats import Statistics
from bandwidth import Bandwidth
from df_firewall import Firewall
from logger import Log


action = sys.argv[1];
bw = Bandwidth()
fw = Firewall()
data = Data()
log = Log(conf.files.limitlog)

if action.upper() == "UPDATE_STATS":

    for row in Data().getIpUser():
        User = row[0]
        ip = row[1]
        stats = Statistics().get_iptables_io(ip)
        if stats:
            tx = stats['bytes_sent']
            rx = stats['bytes_received']
            Connections = Statistics().get_active_connections(ip)
            Data().updateStats(User,Connections, tx, rx)
        else:
            log.error("something went wrong updatings stats, user: "+User+" at "+ip )

if action.upper() == "CHECK_LIMITS":

    soft = bw.is_violating(False)
    hard = bw.is_violating(True)
    
    if(soft[0]):
        print "SOFTLIMIT DOWNSTREAM VIOLATED"
        limitTopFiveDown()
        if(hard[0]):
            print "HARDLIMIT."
            limitAllDown()
    if(soft[1]):
        print "SOFTLIMIT UPSTREAM VIOLATED"
        if(hard[1]):
            print "HARDLIMIT."
    if(soft[2]):
        print "SOFT CONNECTIONLIMIT VIOLATED"
        if(hard[2]):
            print "HARDLIMIT."
    
    if(not soft[0] and not soft[1] and not soft[2]):
        print "NO VIOLATIONS"

        
def activateLimit(users):
    for user in users:
        ip = data.getIP(user[0])[0][0]      ## There is something wierd with that output...
        fw.limit_connections(ip, conf.bandwidth.rx_max_user)
        
        entry = ip + " ("+user + ") limited to "+conf.bandwidth.rx_max_user
        log.info(entry)
        #data.updataUser(SET LIMITED)
        
def limitTopFiveDown():
    activateLimit(data.topFiveDownload())
    
def limitAllDown():
    activateLimit(data.topFiveDownload())
    
def limitTopFiveUp():
    activateLimit(data.topFiveUpload())
    
def limitAllUp():
    activateLimit(data.topFiveDownload())
    
def limitTopFiveConn():
    activateLimit(data.topFiveConnections())
    
def limitAllConn():
    activateLimit(data.topFiveDownload())

