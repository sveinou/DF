#!/usr/bin/env python
 
import sys, time
import subprocess
from DNF.daemon import Daemon
from DNF.stats.con_status import Con
from DNF.stats.df_user_stats import Statistics as stats
from DNF.database.df_data import Data
from DNF.conf import bandwidth
from DNF.firewall.df_firewall import Firewall
 
class dynfd(Daemon):
        def run(self):
                while True:
			
                      #self.rm_limit()
			time.sleep(10)
                        self.update_stats()
                        time.sleep(20)
                        self.update_stats()
			time.sleep(10)
                        self.limit()
			time.sleep(10)

	def update_stats(self):
		clients = Data().get_all_active_clients()
		for client in clients:
			user = client[0]
			ip4 = client[2]
			connections = stats().get_active_connections(ip4)
			io = stats().get_iptables_io(ip4)
			tx = io['bytes_sent']
			rx = io['bytes_received']
			Data().updateStats(user,connections,tx,rx)
		return

	def limit(self):
		if not Con().is_hig_latency():
			return
		else:
			down_clients = Data().aboveDownLimit(bandwidth().rx_max_user)
			for client in down_clients:
				user = client[0]
				ip4 = client[1]
				Firewall().limit_rx(ip)
			
			upl_clients = Data().aboveUpLimit(bandwidth().tx_max_user)
			for client in upl_clients:
                        	user = client[0]
                        	ip4 = client[1]
                        	Firewall().limit_tx(ip)
			conn_clients = Data().aboveConnectionLimit(bandwidth().max_connections_user)
			for client in conn_clients:
                        	user = client[0]
                        	ip4 = client[1]
                        	Firewall().limit_connections(ip)

 		return

	def rm_limit(self):
		Firewall().rm_all_limit()
	
		return


if __name__ == "__main__":
        daemon = dynfd('/tmp/daemon-example.pid','/opt/DF/init.d/1.txt','/opt/DF/init.d/1.txt','/opt/DF/init.d/1.txt')
	if len(sys.argv) == 2:
                if 'start' == sys.argv[1]:
                        daemon.start()
                elif 'stop' == sys.argv[1]:
                        daemon.stop()
                elif 'restart' == sys.argv[1]:
                        daemon.restart()
                else:
                        print "Unknown command"
                        sys.exit(2)
                sys.exit(0)
        else:
                print "usage: %s start|stop|restart" % sys.argv[0]
                sys.exit(2)
