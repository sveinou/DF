## This file defines constants used in DNF. 
# Most constants are defined from /etc/dnf/dnf.conf

from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
try:
    parser.read("/etc/dnf/dnf.conf")
except IOError:
    print("CONFIG NOT FOUND IN /etc/dnf/dnf.conf")
    exit(9)

if not parser.read("/etc/dnf/dnf.conf"):
    print("CONFIG NOT FOUND IN /etc/dnf/dnf.conf")
    exit(9)
    
# globale

server = parser.get("global", "server")

# database
class db:
    server = parser.get("database", "server") 
    user = parser.get("database", "user")#name of database user
    name = parser.get("database", "name") #name of database name
    pw = parser.get("database", "password")	#database password (mabeh an hased value 4 later??)


## DHCP-server
class files:
    leasefile = parser.get("files", "dhcp_leasefile")
    ip_conntrack = parser.get("files", "ip_conntrack")

    defaultlog = parser.get("logs", "default")
    limitlog = parser.get("logs", "limit")
    droplog = parser.get("logs", "drop")
    loginlog = parser.get("logs", "login")
    errorlog = parser.get("logs", "error")

class bandwidth:
    rx_limit_soft = parser.getint("bandwidth", "rx_limit_soft")
    rx_limit_hard = parser.getint("bandwidth", "rx_limit_hard")
    tx_limit_soft = parser.getint("bandwidth", "tx_limit_soft")
    tx_limit_hard = parser.getint("bandwidth", "tx_limit_hard")
    max_connections_soft = parser.getint("bandwidth", "max_connections_soft")
    max_connections_hard = parser.getint("bandwidth", "max_connections_soft")

    max_connections_user = parser.getint("bandwidth", "max_connections_user") 
    rx_max_user = parser.getint("bandwidth", "rx_max_user")
    tx_max_user = parser.getint("bandwidth", "tx_max_user")

    latency_test_addr = parser.get("bandwidth","latency_test_addr")
    latency_hig = parser.getint("bandwidth", "latency_high")  # in ms, if latency > latency_hig return " latency is hig"

    download_file_addr = parser.get("bandwidth", "download_file_addr") # file to test download speed, preff arround 10 mb
    download_time_hig =  parser.getint("bandwidth", "download_time_high") # in seconds, if download_time > download_time_hig return " download time higer than normal"
    
    
## Filters used in the firewall.
#  Don't mess with this, unless you REALLY KNOW what you are doing.
#  

class filter:
    ipv4_in_leasefile = r'(\ [\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3})'
    mac_in_leasefile = r'([a-f|0-9][a-f|0-9]\:[a-f|0-9][a-f|0-9]\:[a-f|0-9][a-f|0-9]\:[a-f|0-9][a-f|0-9]\:[a-f|0-9][a-f|0-9]\:[a-f|0-9][a-f|0-9])'
    mac_exact = ''
    ipv4_exact = r'(^[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}$)'


class exit_status:
    login_error = 1
    ip_mac_mismatch_error = 2
    input_error = 3
    other_exception = 9

    user_already_logged_in = 10 

