#   PYTHONPATH=`pwd` python testdaemon.py start

import logging
import time
from daemon import runner
import subprocess
import DNF.conf as conf

class App():
   
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty' #change to a logfile or /dev/null
        self.stderr_path = '/dev/tty' #change to a logfile or /dev/null
        self.pidfile_path =  '/var/run/dynfwd/dynfwd.pid'
        self.pidfile_timeout = 5
            
    def run(self):
        count=0
        while True:
         #logger.debug("Debug message") #(logging.DEBUG to enable)
         #logger.info("Info message")
         #logger.warn("Warning message")
         #logger.error("Error message")
	 if count == 15: # count 15*20sec= 5min
  	    subprocess.call("/usr/local/bin/dynfw FLUSH LIMITED", shell=True)
	    count = 0

	 if count == 6 and conf.mode != "manual" or count == 12 and conf.mode != "manual": 
     	     subprocess.call("/usr/local/bin/dynfw LIMIT AUTO", shell=True)
	     if conf.mode == "auto":
	         subprocess.call("/usr/local/bin/dynfw LIMIT", shell=True)



	 subprocess.call("/usr/local/bin/dynfw UPDATE", shell=True)
	 count += 1
	 time.sleep(1)



app = App()
logger = logging.getLogger("DaemonLog")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("/var/log/dnf/dynfwd.log")
handler.setFormatter(formatter)
logger.addHandler(handler)

daemon_runner = runner.DaemonRunner(app)
#This ensures that the logger file handle does not get closed during daemonization
daemon_runner.daemon_context.files_preserve=[handler.stream]
daemon_runner.do_action()
