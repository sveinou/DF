#!/usr/bin/python

import subprocess
from time import time
import os
from DNF.conf import bandwidth as bw
from DNF.stats.df_user_stats import Statistics as stats
from DNF.gui import Gui

class Con:

    #returns latency in ms
    def get_ping(self,address):

        ms = 0.0
        p = subprocess.Popen(["ping","-c", "4", address], stdout = subprocess.PIPE)
        for word in p.communicate()[0].split(' '):
            if "time" in word and "=" in word:
                ms += float(word.split("=")[1])
        return ms/4

    def ping_cal(self,address):
        ms = 0.0
        times = 100
        for i in range(times):
            Gui().loadingbar(i,"latency test")
            DEVNULL = open(os.devnull, 'w')
            p = subprocess.Popen(["ping","-c", "1", address], stdout = subprocess.PIPE, stderr = DEVNULL)
            for word in p.communicate()[0].split(' '):
                if "time" in word and "=" in word:
                    ms += float(word.split("=")[1])
        Gui().loadingbar(100,"finished! ")
        return ms/times

    #returns how long it takes to download given file in secs
    def download_time(self,address):
        filename = address.split('/')[-1]
        first = time()
        fh = open("NUL","w")
        subprocess.call(["wget",address],stdout = fh, stderr = fh)
        fh.close()
        after = time()
        subprocess.call("rm NUL " + filename,shell=True)
        return after - first    


    def is_slow(self):
        time = self.download_time(bw.download_file_addr)
        if time > bw.download_time_hig:
            return True
        else:
            return False

    def is_hig_latency(self):
        ms = self.get_ping(bw.latency_test_addr)
        if ms > bw.latency_hig:
            return True
        else:
            return False

    def inferface_ip(self,interface):
        ifc = subprocess.Popen(["ifconfig",interface], stdout = subprocess.PIPE)
        ifc = ifc.communicate()[0]
        IP = ""
        for word in ifc.split():
            if "addr:" in word:
                    if len(word.split("."))==4: IP = word.split(":")[1]
                    break
        return IP

    
            

    def find_if(self):
        DEVNULL = open(os.devnull, 'w')
        ifconfig = subprocess.Popen(["ifconfig"], stdout=subprocess.PIPE, stderr=DEVNULL)
        ifconfig = ifconfig.communicate()[0].split()
        prev_word = ifconfig[0]
        interfaces = ""
        for word in ifconfig:
            if word == "Link" and prev_word != "lo" and prev_word != "Link":
                interfaces += " " + prev_word
                
            prev_word = word
        internal = ""
        external = ""
        
        for interface in interfaces.split():
            x = int(interfaces.index(interface)) + 1
            x = int(100 / len(interfaces) * x)
            Gui().loadingbar(x)

            if interface:
                try:
                    DEVNULL = open(os.devnull, 'w')
                    ping = subprocess.Popen(["/bin/ping", "-c", "1", "-I", interface, "8.8.8.8"], stdout=subprocess.PIPE, stderr=DEVNULL)
                    ping = ping.communicate()[0]
                    if "64" in ping:
                        external = interface
                    else:
                        internal = interface

                except Exception, e:
                    internal = interface
                            
        Gui().loadingbar(100)
        return{'ext':external, 'int':internal}
