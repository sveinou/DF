## This file defines constants used in DNF. 
# Most constants are defined from /etc/dnf/dnf.conf
import logging
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
external_ip = '10.10.10.101'
internal_ip = '10.20.30.40'

internal_interface = parser.get("global", "internal_interface")
external_interface = parser.get("global", "external_interface")
mode = parser.get("global", "mode")
# database
singel = parser.getboolean("global", "singel_login")

class log:
    _level = parser.get("logs", "loglevel")
    level = logging.DEBUG
    if _level.upper() == 'INFO':
        level = logging.INFO
    elif _level.upper == 'WARNING':
        level = logging.WARNING
    elif _level == 'ERROR':
        level = logging.ERROR
    elif _level.upper() == 'CRITICAL':
        level = logging.CRITICAL
    
    #logformat = logging.Formatter(' %(levelname)s : %(asctime)s - %(name)s - %(message)s')
    _default = parser.get("logs", "default")
    _users = parser.get("logs", "access")
    _web = parser.get("logs", "webservice")
    console = logging.StreamHandler()
    default = None
    users = None
    web = None
    
    try:
        default = logging.FileHandler(filename=_default)
    except IOError:
        default = console
    try:
        users = logging.FileHandler(filename=_users)
    except IOError:
        users = console
    try:
        web = logging.FileHandler(filename=_web)
    except IOError:
        web = console
    
class db:
    server = parser.get("database", "server") 
    user = parser.get("database", "user")#name of database user
    name = parser.get("database", "name") #name of database name
    pw = parser.get("database", "password")
    port = parser.get("database", "port") 
    
## DHCP-server
class files:
    leasefile = parser.get("files", "dhcp_leasefile")
    ip_conntrack = parser.get("files", "ip_conntrack")

#     defaultlog = parser.get("logs", "default")
#     limitlog = parser.get("logs", "limit")
#     droplog = parser.get("logs", "drop")
#     loginlog = parser.get("logs", "login")
#     errorlog = parser.get("logs", "error")
#     djangolog = parser.get("logs", "webservice")

class bandwidth:
    unit = parser.get("bandwidth", "unit")
    max_rxs = parser.getint("bandwidth", "max_rxs")
    max_txs = parser.getint("bandwidth", "max_txs")
    max_connections = parser.getint("bandwidth", "max_connections")

    latency_test_addr = parser.get("bandwidth","latency_test_addr")
    latency_hig = parser.getint("bandwidth", "latency_high")  # in ms, if latency > latency_hig return " latency is hig"
    limit_offsett = parser.getfloat("bandwidth", "limit_offsett")

    download_file_addr = parser.get("bandwidth", "download_file_addr") # file to test download speed, preff arround 10 mb
    download_time_hig =  parser.getint("bandwidth", "download_time_high") # in seconds, if download_time > download_time_hig return " download time higer than normal"
    
    
## Filters used in the firewall.
#  Don't mess with this, unless you REALLY KNOW what you are doing.
#  .. and even then. STAY AWAY.

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


