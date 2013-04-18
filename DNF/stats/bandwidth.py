import time, subprocess, os					#python modules
from DNF.stats import info
from DNF import conf

class Bandwidth():
#	lncmd = 'lnstat -s0 -i1 -c-1 -k rt_cache:in_hit,rt_cache:out_hit >> bwfile'

    def read(self, seconds=10):
        """
        Reads bandwidth from lnstat
        """

        ln_out_cmd = 'lnstat -s0 -i1 -c-1 -k rt_cache:out_hit >> bwout'
        ln_in_cmd = 'lnstat -s0 -i1 -c-1 -k rt_cache:in_hit >> bwin'

        subprocess.Popen(ln_out_cmd, shell=True)
        subprocess.Popen(ln_in_cmd, shell=True)
        time.sleep(seconds)
        
        subprocess.Popen("killall lnstat", shell=True)

        bwin = open('bwin').read().split('\n')
        bwout = open('bwout').read().split('\n')
        
        bwin = [int(number[:-1]) for number in bwin if number.strip() != ''] #remove anything empty
        bwout = [int(number[:-1]) for number in bwout if number.strip() != '']    #remove anything emptry
        

#CLEANUP	
        subprocess.Popen("rm bwin", shell=True)
        subprocess.Popen("rm bwout", shell=True)

        return (bwin, bwout)


    def avg(self, time=10):
        """
        Calculates average bandwidth
        """
       
        bwin, bwout = self.read(time)
        
        bwin.pop(0)      #First is garbage
        bwout.pop(0)
        
        avgin = 0
        for point in bwin:
            avgin += point
        avgin = avgin/len(bwin)
        
        avgout = 0
        for point in bwout:
            avgout += point
        avgout = avgout / len(bwout)

        return {'in':avgin,'out':avgout}

    def is_violating(self, hard=False, rx_limit=0, tx_limit=0, connections=0):
        """
        Checks if any of the limits are being violated.
        """
        
        if rx_limit == 0:
            rx_limit = conf.bandwidth.rx_limit_hard if hard else conf.bandwidth.rx_limit_soft
        if tx_limit == 0:
            tx_limit = conf.bandwidth.tx_limit_hard if hard else conf.bandwidth.tx_limit_soft
        if connections == 0:
            connections = conf.bandwidth.max_connections_hard if hard else conf.bandwidth.max_connections_soft
        avg = self.avg(5)
        s = info.System()
        con = s.connection_load()
        
        return ((avg['in'] > rx_limit), (avg['out'] > tx_limit), (connections < con))
        
    def find_violators(self, hard = False):
        rx_limit = conf.bandwidth.rx_limit_hard if hard else conf.bandwidth.rx_limit_soft
        tx_limit = conf.bandwidth.tx_limit_hard if hard else conf.bandwidth.tx_limit_soft
        connections = conf.bandwidth.max_connections_hard if hard else conf.bandwidth.max_connections_soft
        
        return "Something from database"
        
