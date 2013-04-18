#from datetime import datetime
#import sys, os, time
from DNF import conf
import time
from DNF.database.storage import Database

class Data:
    db = Database()
    
    def __init__(self):
        pass

    def getIp4(self, ip4):
        sql = "select * from clients where IP4='%s'" % ip4
        return self.db.get_row(sql)

    def get_stats(self, user):
	sql = "select * from stats where User='%s'" % user
	return self.db.get_row(sql)
  
    def get_limited(self, user):
	sql = "select * from limited where User='%s'" % user
	return self.db.get_row(sql)

    def get_all_active_clients(self):
    	sql = "select * from clients where Active=1"
    	return self.db.get_all_rows(sql)
 
    def all_active_ips(self):
        sql = "SELECT ip4 FROM clients WHERE active = 1"
        return [row[0] for row in self.db.get_all_rows(sql)]
    
    def active(self, data_type, search):
        print str(type(search))
        if type(search) == str:
            sql = "select Active from clients where %s='%s'" % (data_type,search)
        else:
            # obs. maa vite type i database
            sql = "select Active from clients where %s={1}" % (data_type,search) 

        sql = self.db.get_row(sql)
        if sql:
            if sql[0] == 1:
                return True
        else:
            return False

    def get_info_client(self,get_type,search_type,search):

        if type(search) == str:
            sql = "select %s from clients where %s='%s'" % (get_type,search_type,search)
        else:
            # obs. maa vite type i database
            sql = "select %s from clients where %s={1}" % (get_type,search_type,search)

        return self.db.get_row(sql)

    def DbAddRow(self,user,mac,ip4,ip6='Not in use'):

        #add a new user, or updating an exsiting one

        if len(mac) != 17 and len(ip4) < 7 and len(ip4) > 17:
            raise ValueError("somthing od with ip4/mac")
        elif self.get_info_client("user","user",user):
            sql = "UPDATE clients set Mac='%s', IP4='%s', IP6='%s', Active=1 WHERE User='%s'" % (mac,ip4,ip6,user) 
        else:
            sql = "INSERT INTO clients VALUES ('%s', '%s', '%s', '%s', 1) " % (user,mac,ip4,ip6)
        self.db.alter(sql)

    def mark_user_active(self,user,mac,ip):
        activelist = "select ip4, mac, user from clients where Active = 1"
        activelist = self.db.get_all_rows(activelist)
        ips = [row[0] for row in activelist]
        macs = [row[1] for row in activelist]
        
        if conf.singel:
            users = [row[2] for row in activelist]
            if user in users:
                return (False, ip, mac, user)
            
        if ip in ips or mac in macs:
            return (False, ip, mac, user)
        
        self.DbAddRow(user, mac, ip)
        
        return (True, ip, mac, user)



    def DbActiveUser(self,user,active):

    #acitvates or deactivates an user
 

        sql = "UPDATE clients SET Active=%s WHERE User='%s'" % (active,user)
            
        self.db.alter(sql)

    def DbActiveIp4(self, ip4, active):
        sql ="UPDATE clients SET Active=%i WHERE IP4='%s'" % (active,ip4)
        self.db.alter(sql)

    def DbUpdateRow(self,user,data):

    #updates one part in a user`s row

     # maybeh make a better check for it...


        if len(data) > 17:
            type = "IP6"
        elif len(data) == 17:
            type = "Mac"
        elif len(data) > 7:
            type = "IP4"
        else:
            raise ValueError("input error")

        sql = "UPDATE clients SET %s='%s', Active=1 WHERE User='%s'" % (type,data,user)

        self.db.alter(sql)
    

    def updateStats(self, user, connections, tx, rx):
    
        sql = "select tx_total, rx_total, UNIX_TIMESTAMP(Time) from stats where User='%s'" % (user)
        row = Database().get_row(sql)    
        if row:
            tx_total = tx + row[0]
            rx_total = rx + row[1]
            sec = int(time.time() - row[2])
            sql= "UPDATE stats SET Connections=%i, tx_total=%i, rx_total=%i, Time=FROM_UNIXTIME(%s) WHERE User='%s'" % (connections,tx_total,rx_total,time.time(),user) 
            
            
        else:
            Time = time.time()
            sql = "INSERT INTO stats VALUES ('%s', %i, 0, 0, 0, 0,FROM_UNIXTIME(%s))" %(user,connections,Time)

        self.db.alter(sql)
    def update_io(self,io):
	sql = "select * from stats"
	row = Database().get_row(sql)
	if not row:
            return "NO CLIENTS"
	for client in io:
	    #client [ip,tx,rx]
	    sql = "UPDATE stats INNER JOIN clients ON stats.USER = clients.USER SET txs=%i, rxs=%i WHERE clients.IP4='%s'" %(client[1],client[2],client[0])
	    Database().alter(sql)
	return "done!"
	


    def aboveDownLimit(self, limit):
        sql = "SELECT stats.User, clients.IP4 FROM stats join clients on stats.User=clients.User  WHERE stats.rxs > %i" %(limit)
        return Database().get_all_rows(sql)
        
    def aboveUpLimit(self, limit):
        sql = "SELECT stats.User, clients.IP4 FROM stats join clients on stats.User=clients.User  WHERE stats.txs > %i" %(limit)
        return Database().get_all_rows(sql)
        
    def aboveConnectionLimit(self, limit):
        sql = "SELECT stats.User, clients.IP4 FROM stats join clients on stats.User=clients.User  WHERE stats.Connections > %i" %(limit)
        return Database().get_all_rows(sql)

        
    def topFiveDownload(self):
        sql = "SELECT user, IP4 rxs FROM stats ORDER BY rxs DESC LIMIT 5"
        return Database().get_all_rows(sql)

    def topFiveConnections(self):
        sql = "SELECT user, IP4 connections FROM stats ORDER BY connections DESC LIMIT 5"
        return Database().get_all_rows(sql)
    
    def topFiveUpload(self):
        sql = "SELECT user, IP4 txs FROM stats ORDER BY txs DESC LIMIT 5"
        return Database().get_all_rows(sql)
        
    def highscore(self):
        tx_total = "SELECT user, tx_total FROM stats ORDER BY tx_total DESC LIMIT 1"
        rx_total = "SELECT user, rx_total FROM stats ORDER BY rx_total DESC LIMIT 1"
        txs = "SELECT user, txs FROM stats ORDER BY txs DESC LIMIT 1"
        rxs = "SELECT user, rxs FROM stats ORDER BY rxs DESC LIMIT 1"
        con = "SELECT user, connections FROM stats ORDER BY connections DESC LIMIT 1"
        
        tx_total = Database().get_all_rows(tx_total)
        rx_total = Database().get_all_rows(rx_total)
        txs = Database().get_all_rows(txs)
        rxs = Database().get_all_rows(rxs)
        con = Database().get_all_rows(con)



        return (tx_total, rx_total, txs, rxs, con)

    def get_limit(self, User):
        sql = "select * from limited WHERE User='%s'" % User
        return self.db.get_row(sql)
        

    def add_limit(self, ip, limit):        
        User = self.getIp4(ip)[0] # gets the user
        if self.get_limit(User):
            sql = "UPDATE limited SET %s=1 WHERE User='%s'" %(limit,User)
        else:
            sql = "INSERT INTO limited (User, %s) values ('%s',  1)" % (limit,User)

        self.db.alter(sql)
        return

    def rm_all_limit(self): 
        sql = "UPDATE limited SET CONNLIMIT=0, RXLIMIT=0, TXLIMIT=0"
        self.db.alter(sql)
        return
    def rm_limit(self, ip4):
        User = self.getIp4(ip4)[0]
        sql = "update limited set CONNLIMIT=0, RXLIMIT=0, RXLIMIT=0 where User='%s'" % User
        return
    
