#!/usr/bin/env python
 
import sys, time
import subprocess
from DNF.daemon import Daemon
from DNF.stats.con_status import Con
from DNF.stats.df_user_stats import Statistics as stats
from DNF.database.df_data import Data
 
class dynfd(Daemon):
        def run(self):
                while True:
                        self.rm_limit()
                        self.update_stats()
                        time.sleep(5)
                        self.update_stats()
                        self.limit()

	def update_stats(self):

		subprocess.call("echo yay | wall", shell=True)
		file = open("//opt//DF//init.d//test.txt","w")
		

		file.write("yayaaa")
		file.close()
		return

	def limit(self):

 		return

	def rm_limit(self):
	
		return


if __name__ == "__main__":
        daemon = dynfd('/tmp/daemon-example.pid')
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
