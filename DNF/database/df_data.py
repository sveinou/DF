from DNF import conf
import time
from DNF.database.storage import Database as db

class Data:
    """
    This is where all the sql queries are done.
    Methods returns resultsets from the database.  
    """

    #db = Database()
    
    def __init__(self):
        pass

    def get_ip4(self, ip4): 
        sql = "select * from clients where IP4='%s'" % ip4
        return db().get_row(sql)

    def get_stats(self, user):
        sql = "select * from stats where User='%s'" % user
        return db().get_row(sql)
  
    def get_limited(self, user):
        sql = "select * from limited where User='%s'" % user
        return db().get_row(sql)

    def get_all_active_clients(self):
        sql = "select * from clients where Active=1"
        return db().get_all_rows(sql)
 
    def all_active_ips(self):
        sql = "SELECT ip4 FROM clients WHERE active = 1"
        return [row[0] for row in db().get_all_rows(sql)]
    
    def active(self, data_type, search):
        print str(type(search))
        if type(search) == str:
            sql = "select Active from clients where %s='%s'" % (data_type,search)
        else:
            # need to know the database data type
            sql = "select Active from clients where %s={1}" % (data_type,search) 

        sql = db().get_row(sql)
        if sql:
            if sql[0] == 1:
                return True
        else:
            return False

    def get_info_client(self,get_type,search_type,search):

        if type(search) == str:
            sql = "select %s from clients where %s='%s'" % (get_type,search_type,search)
        else:
            # need to know the database data type
            sql = "select %s from clients where %s={1}" % (get_type,search_type,search)

        return db().get_row(sql)

    def add_row(self,user,mac,ip4,ip6='Not in use'): #DbAddRow

        #add a new user, or updating an exsiting one

        if len(mac) != 17 and len(ip4) < 7 and len(ip4) > 17:
            raise ValueError("somthing od with ip4/mac")
        elif self.get_info_client("user","user",user):
            sql = "UPDATE clients set Mac='%s', IP4='%s', IP6='%s', Active=1 WHERE User='%s'" % (mac,ip4,ip6,user) 
        else:
            sql = "INSERT INTO clients VALUES ('%s', '%s', '%s', '%s', 1) " % (user,mac,ip4,ip6)
        db().alter(sql)

    def mark_user_active(self,user,mac,ip):
        activelist = "select ip4, mac, user from clients where Active = 1"
        activelist = db().get_all_rows(activelist)
        ips = [row[0] for row in activelist]
        macs = [row[1] for row in activelist]
        
        if conf.singel:
            users = [row[2] for row in activelist]
            if user in users:
                return (False, ip, mac, user)
            
        if ip in ips or mac in macs:
            return (False, ip, mac, user)
        
        self.add_row(user, mac, ip)
        
        return (True, ip, mac, user)



    def active_user(self,user,active): #DbActiveUser

    #acitvates or deactivates an user
 

        sql = "UPDATE clients SET Active=%s WHERE User='%s'" % (active,user)
            
        db().alter(sql)

    def active_ip4(self, ip4, active): #DbActiveIp4
        sql ="UPDATE clients SET Active=%i WHERE IP4='%s'" % (active,ip4)
        db().alter(sql)

    def update_row(self,user,data): #DbUpdateRow

    #updates one part in a user`s row

    # maybeh make a better check for it...


        if len(data) > 17:
            q = "IP6"
        elif len(data) == 17:
            q = "Mac"
        elif len(data) > 7:
            q = "IP4"
        else:
            raise ValueError("input error")

        sql = "UPDATE clients SET %s='%s', Active=1 WHERE User='%s'" % (q,data,user)

        db().alter(sql)
    

    def update_stats(self, user, connections, tx, rx): #updateStats
        

        if not connections:
            connections = 0
        sql = "select tx_total, rx_total, UNIX_TIMESTAMP(Time) from stats where User='%s'" % (user)
        row = db().get_row(sql)    
        if row:
            tx_total = tx + row[0]
            rx_total = rx + row[1]
            sec = int(time.time() - row[2])
            sql= "UPDATE stats SET Connections=%i, tx_total=%i, rx_total=%i, Time=FROM_UNIXTIME(%s) WHERE User='%s'" % (int(connections),int(tx_total),int(rx_total),time.time(),user) 
            
            
        else:
            Time = time.time()
            sql = "INSERT INTO stats VALUES ('%s', %i, 0, 0, 0, 0,FROM_UNIXTIME(%s))" %(user,connections,Time)

        db().alter(sql)
        
    def update_io(self,io):
        sql = "select * from stats"
        row = db().get_row(sql)
        if not row:
                return "NO CLIENTS"
        for client in io:
            sql = "UPDATE stats INNER JOIN clients ON stats.USER = clients.USER SET txs=%i, rxs=%i WHERE clients.IP4='%s'" %(client[1],client[2],client[0])
            db().alter(sql)
        return "done!"
    


    def above_down_limit(self, limit): #aboveDownLimit
        sql = "SELECT stats.User, clients.IP4 FROM stats join clients on stats.User=clients.User  WHERE stats.rxs > %i" %(limit)
        return db().get_all_rows(sql)
        
    def above_up_limit(self, limit):
        sql = "SELECT stats.User, clients.IP4 FROM stats join clients on stats.User=clients.User  WHERE stats.txs > %i" %(limit)
        return db().get_all_rows(sql)
        
    def above_connection_limit(self, limit):
        sql = "SELECT stats.User, clients.IP4 FROM stats join clients on stats.User=clients.User  WHERE stats.Connections > %i" %(limit)
        return db().get_all_rows(sql)

        
    def top_five_download(self):
        sql = "SELECT user, IP4 rxs FROM stats ORDER BY rxs DESC LIMIT 5"
        return db().get_all_rows(sql)

    def top_five_connections(self):
        sql = "SELECT user, IP4 connections FROM stats ORDER BY connections DESC LIMIT 5"
        return db().get_all_rows(sql)
    
    def top_five_upload(self):
        sql = "SELECT user, IP4 txs FROM stats ORDER BY txs DESC LIMIT 5"
        return db().get_all_rows(sql)
        
    def highscore(self):
        tx_total = "SELECT user, tx_total FROM stats ORDER BY tx_total DESC LIMIT 1"
        rx_total = "SELECT user, rx_total FROM stats ORDER BY rx_total DESC LIMIT 1"
        txs = "SELECT user, txs FROM stats ORDER BY txs DESC LIMIT 1"
        rxs = "SELECT user, rxs FROM stats ORDER BY rxs DESC LIMIT 1"
        con = "SELECT user, connections FROM stats ORDER BY connections DESC LIMIT 1"
        
        tx_total = db().get_all_rows(tx_total)
        rx_total = db().get_all_rows(rx_total)
        txs = db().get_all_rows(txs)
        rxs = db().get_all_rows(rxs)
        con = db().get_all_rows(con)



        return (tx_total, rx_total, txs, rxs, con)

    def get_limit(self, User):
        sql = "select * from limited WHERE User='%s'" % User
        return db().get_row(sql)

    def count_limited(self, limit_type):
        sql = "select count(*) from limited WHERE %s=1" % limit_type #CONNLIMIT, RXLIMIT, TXLIMIT  
        return db().get_row(sql)

    def add_limit(self, ip, limit):        
        User = self.get_ip4(ip)[0] # gets the user
        if self.get_limit(User):
            sql = "UPDATE limited SET %s=1 WHERE User='%s'" %(limit,User)
        else:
            sql = "INSERT INTO limited (User, %s) values ('%s',  1)" % (limit,User)

        db().alter(sql)
        return

    def rm_all_limit(self): 
        sql = "UPDATE limited SET CONNLIMIT=0, RXLIMIT=0, TXLIMIT=0"
        db().alter(sql)
        return
       
    def rm_limit(self, ip4):
        User = self.get_ip4(ip4)[0]
        sql = "update limited set CONNLIMIT=0, RXLIMIT=0, RXLIMIT=0 where User='%s'" % User
        db().alter(sql)
        return
    
