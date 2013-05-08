import sys,datetime
from DNF import conf

class Log():
    
    def __init__(self, logfile=conf.log.default):
        self.logfile = logfile
        self.errorlog = conf.log.default

    def info(self, logentry):
        try:
            log = open(self.logfile, mode='a')
            timestamp = str(datetime.datetime.now())
            logentry = timestamp + ": " + logentry + "\n"
            log.write(logentry)
        except IOError, err:
            print "CANNOT WRITE TO LOGFILE %s \n %s" % (self.logfile, err)
        
        
    def error(self,logentry):
        try:
            log = open(self.errorlog, mode='a')	
            timestamp = str(datetime.datetime.now())
            logentry = timestamp + ": " + logentry + "\n"
            log.write(logentry)
        except IOError, err:
             print "CANNOT WRITE TO LOGFILE %s \n %s" % (self.errorlog, err)
        
