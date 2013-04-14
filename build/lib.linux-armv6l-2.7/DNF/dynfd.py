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

	    subprocess.call("/usr/local/bin/dynfw UPDATE", shell=True)
	    time.sleep(20)
	    subprocess.call("/usr/local/bin/dynfw FLUSH LIMITED", shell=True)
	    time.sleep(20)
	    subprocess.call("/usr/local/bin/dynfw UPDATE", shell=True)
	    time.sleep(20)
	    subprocess.call("/usr/local/bin/dynfw LIMIT", shell=True)
	    time.sleep(30)



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
