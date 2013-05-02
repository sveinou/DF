import subprocess
from DNF.database.df_data import Data
from DNF import conf
from string import upper
class Firewall:
    """
    Sends commands to iptables to alter chains
    """

    def __init__(self):
        pass

    def accept_ip4(self, ipv4_addr):
        """
        Opens iptables FORWARD and PRERPOUTING chain for ipaddress
        
        Keywords arguments:
        ipv4_addr -- IPv4-address to let trough firewall
        """

        rules = ["/sbin/iptables -I ALLOWED -d"+ipv4_addr+" -j ACCEPT",
            "/sbin/iptables -I ALLOWED -s"+ipv4_addr+" -j ACCEPT",
            "/sbin/iptables -t nat -I ALLOWED -d"+ipv4_addr+" -j ACCEPT",
            "/sbin/iptables -t nat -I ALLOWED -s"+ipv4_addr+" -j ACCEPT",]
 
        for rule in rules:
            subprocess.call('sudo '+rule, shell=True)


    def accept_ip6(self, ipv6_addr):
        """
        Tells iptables to let trough IPv6-addess
        
        Keyword Arguments:
        ipv6_addr -- IPv6-address that's welcome trough our firewall
        """
        
        rules = ["/sbin/iptables -I ALLOWED -d"+ipv6_addr+" -j ACCEPT",
          "/sbin/iptables -I ALLOWED -s"+ipv6_addr+" -j ACCEPT",]
        for rule in rules:
            subprocess.call('sudo '+ rule, shell=True)


    def drop_ip4(self, ipv4_addr):
        """
        Removes ip-address from accept-list
        
        Keyword arguments:
        ipv4_addr = IPv4-address to remove
        """
        
        rules = ["/sbin/iptables -D ALLOWED -d"+ipv4_addr+" -j ACCEPT",
            "/sbin/iptables -D ALLOWED -s"+ipv4_addr+" -j ACCEPT",
            "/sbin/iptables -t nat -D ALLOWED -d"+ipv4_addr+" -j ACCEPT",
            "/sbin/iptables -t nat -D ALLOWED -s"+ipv4_addr+" -j ACCEPT",]

        for rule in rules:
            subprocess.call('sudo ' + rule, shell=True)

    def drop_ip6(self, ipv6_addr):
        """
        Removes ipv6-address from iptables accept-list
        
        Keyword arguments:
        ipv6_addr = IPv6 address to remove
        """
        
        rules = ["/sbin/ip6tables -D ALLOWED -d"+ipv6_addr+" -j ACCEPT",
            "/sbin/ip6tables -D ALLOWED -s"+ipv6_addr+" -j ACCEPT",]

        for rule in rules:
            subprocess.call('sudo '+rule, shell=True)   


    def limit_connections(self, ip):
        """
        Adds connectionlimit to user
        """
        rules = ["iptables -I LIMITED -d "+ip+" -j CONNLIMIT",
                 "iptables -I LIMITED -s "+ip+" -j CONNLIMIT"]
        
        for rule in rules:
            subprocess.call('sudo ' + rule, shell=True)   

        
        #update something in the database?
        
        return


    def is_rule(self, ip): #isRule
        """
        Returns true if there is an rule with given ip-addres, 
        if the rule do not exist, it wil return false
        """
        ip6 = subprocess.check_output("sudo /sbin/ip6tables -L -n", shell=True)

        ip4 = subprocess.check_output("sudo /sbin/iptables -L -n", shell=True)
        ip4_nat = subprocess.check_output("sudo /sbin/iptables -t nat -L -n ", shell=True)

        if ip in ip4 or ip in ip6 or ip in ip4_nat:
            return True
        else:
            return False
        
    def get_custom_forward(self):
        """
        returns all rules in limited-chain.        
        """
        ipcmd = ['sudo', 'iptables', '-nvxL', 'CUSTOM_FORWARD']
        ipres  = subprocess.Popen(ipcmd, stdout=subprocess.PIPE).communicate()[0].split("\n")
        rules = []
        
        for rule in [line.split() for line in ipres[2:-1]]:
            dpt = 'any' 
            spt = 'any'
            rest = ''
            for opt in rule[9:]:
                if opt[:3] == 'dpt': dpt = opt[4:]
                elif opt[:3] == 'spt': spt = opt[4:]
                else: rest += opt
            rules.append({'pkts':rule[0], 'bytes':rule[1],
                          'target':rule[2],'prot':rule[3],
                          'opt':rule[4],'in':rule[5],
                          'out':rule[6],'src':rule[7],
                          'dst':rule[8], 'dpt':dpt, 'spt':spt, 'rest':rest})
            
        return rules;
    
    def get_custom_input(self):
        """
        returns all rules in limited-chain.        
        """
        ipcmd = ['sudo', 'iptables', '-nvxL', 'CUSTOM_INPUT']
        ipres  = subprocess.Popen(ipcmd, stdout=subprocess.PIPE).communicate()[0].split("\n")
        rules = []
        for rule in [line.split() for line in ipres[2:-1]]:
            dpt = 'any' 
            spt = 'any'
            rest = ''
            for opt in rule[9:]:
                if opt[:3] == 'dpt': dpt = opt[4:]
                elif opt[:3] == 'spt': spt = opt[4:]
                else: rest += opt
            rules.append({'pkts':rule[0], 'bytes':rule[1],
                          'target':rule[2],'prot':rule[3],
                          'opt':rule[4],'in':rule[5],
                          'out':rule[6],'src':rule[7],
                          'dst':rule[8], 'dpt':dpt, 'spt':spt, 'rest':rest})
            
        return rules;
    
    def add_custom_rule(self,chain, src, src_port=None, dst=conf.external_interface, dst_port=None, target='FORWARD'):
        """
        Constructs rule according to input. requires chain, source and target.
        If no destination is given, system presumes it's external interface as destination. 
        """
        if not (chain and src and target and dst):
            return False
        
        #Construction
        rule = "sudo /sbin/iptables -I "+upper(chain)   
        rule += " -s "+src
        if src_port: rule += " --sport "+src_port
        rule += " -d "+dst
        if dst_port: rule += " --dport "+dst_port
        rule += " -j "+upper(target)
        
        #Send rule
        subprocess.call(rule, shell=True)
        return True
        
    def get_limited(self):
        """
        returns all rules in limited-chain.        
        """
        ipcmd = ['sudo', 'iptables', '-nvxL', 'LIMITED']
        ipres  = subprocess.Popen(ipcmd, stdout=subprocess.PIPE).communicate()[0].split("\n")
        return [line.split() for line in ipres[2:-1]]
    
    def get_allowed(self):
        """
        Returns all rules in allowed-chain
        """
        ipcmd = ['sudo', 'iptables', '-nvxL', 'ALLOWED']
        ipres  = subprocess.Popen(ipcmd, stdout=subprocess.PIPE).communicate()[0].split("\n")
        return [line.split() for line in ipres[2:-1]]


    def rm_limit(self, ip):
        """
        just incase there are duplicate enteries of somthing that shouldnt happen
        """

        ipt = subprocess.Popen(['sudo', "iptables","-L", "LIMITED"], stdout = subprocess.PIPE)
        grep = subprocess.Popen(["grep", ip], stdin=ipt.stdout, stdout = subprocess.PIPE)
        out = grep.communicate()[0]
        for rule in out.split("\n"):
            rule = rule.split("all")[0]
            print rule
            if rule == "RXLIMIT":
                subprocess.call("sudo /sbin/iptables -D LIMITED -d "+ip+" -j "+rule, shell=True)
            elif rule == "TXLIMIT":
                subprocess.call("sudo /sbin/iptables -D LIMITED -s "+ip+" -j "+rule, shell=True)
            else: # will try to remove tvice as manny rules as there are,
                subprocess.call("sudo /sbin/iptables -D LIMITED -s "+ip+" -j "+rule, shell=True)
                subprocess.call("sudo /sbin/iptables -D LIMITED -d "+ip+" -j "+rule, shell=True) 
    
        Data().rm_limit(ip)
        return
        
    def rm_all_limit(self):
        subprocess.call("sudo /sbin/iptables -F LIMITED", shell=True)
        Data().rm_all_limit()
        
        
    def limit_rx(self, ip):
        subprocess.call("sudo /sbin/iptables -I LIMITED -d "+ip+" -j RXLIMIT", shell=True) 
        Data().add_limit(ip,"RXLIMIT")
        return

    def limit_tx(self, ip):
        subprocess.call("sudo /sbin/iptables -I LIMITED -s "+ip+" -j TXLIMIT", shell=True) 
        Data().add_limit(ip,"TXLIMIT")
