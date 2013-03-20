

# globale

server = "localhost"

# database
class db:
    server = "localhost" #name of your mysql Server
    user = "df" #name of database user
    name = "df" #name of database name
    pw = "df"	#database password (mabeh an hased value 4 later??)


## DHCP-server
class files:
    leasefile = "/var/lib/dhcp/dhcpd.leases"
    ip_conntrack = "/proc/net/ip_conntrack"

    defaultlog = "/var/log/dfw/collect.log"
    limitlog = "/var/log/dfw/limited.log"
    droplog = "/var/log/dfw/drop.log"
    loginlog = "/var/log/dfw/login.log"
    errorlog = "/var/log/dfw/error.log"

class bandwidth:
    rx_limit_soft = 50 #50*1024 # in k bytes
    rx_limit_hard = 100*1024 # in k bytes
    tx_limit_soft = 50 #50*1024 # in k bytes
    tx_limit_hard = 100*1024 # in k bytes    
    max_connections_soft = 500*100
    max_connections_hard = 1000*100

    max_connections_user = 1000 
    rx_max_user = 20*1024*1024 # in bytes
    tx_max_user = 20*1024*1024 # in bytes
    
    
    
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

