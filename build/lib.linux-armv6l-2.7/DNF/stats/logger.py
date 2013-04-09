
import sys,datetime
from DNF import conf

class Log():
    
    def __init__(self, logfile=conf.files.defaultlog):
        self.logfile = logfile
        self.errorlog = conf.files.errorlog

    def info(self, logentry):
        log = open(self.logfile, mode='a')
        timestamp = str(datetime.datetime.now())
        logentry = timestamp + ": " + logentry + "\n"
        log.write(logentry)
        
    def error(self,logentry):
        log = open(self.errorlog, mode='a')	
        timestamp = str(datetime.datetime.now())
        logentry = timestamp + ": " + logentry + "\n"
        log.write(logentry)
