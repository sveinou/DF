#   PYTHONPATH=`pwd` python testdaemon.py start

import logging
import time
from daemon import runner
import subprocess
from DNF.stats.con_status import Con
from DNF.stats.df_user_stats import Statistics as stats
from DNF.database.df_data import Data
from DNF.conf import bandwidth
from DNF.firewall.df_firewall import Firewall


class App():
    
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/var/run/dynfwd/dynfwd.pid'
        self.pidfile_timeout = 5
            
    def run(self):
        while True:
            #Main code goes here ...
            #Note that logger level needs to be set to logging.DEBUG before this shows up in the logs
            #logger.debug("Debug message")
            #logger.info("Info message")
            #logger.warn("Warning message")
            #logger.error("Error message")

    	    logger.debug("trying to remove all limit rules")
	    self.rm_limit()
	    logger.debug("trying to runn update_stats")
	    self.update_stats()
	    time.sleep(30)
	    logger.debug("trying to updating stats")
	    self.update_stats()
	    logger.debug("trying to run limited")
	    self.limit()
	

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


app = App()
logger = logging.getLogger("DaemonLog")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("/var/log/dfw/dynfwd.log")
handler.setFormatter(formatter)
logger.addHandler(handler)

daemon_runner = runner.DaemonRunner(app)
#This ensures that the logger file handle does not get closed during daemonization
daemon_runner.daemon_context.files_preserve=[handler.stream]
daemon_runner.do_action()
