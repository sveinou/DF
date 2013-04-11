#!/usr/bin/env python
 
import sys, time
import subprocess
from DNF.daemon import Daemon
from DNF.stats.conn_status import Con
 
class dynfd(Daemon):
        def run(self):
                while True:
			Con().check()
                        time.sleep(10)
 
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
