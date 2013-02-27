

# global

server = "localhost"

# database
class db:
    server = "localhost" #name of your mysql Server
    user = "df" #name of database user
    name = "df" #name of database name
    pw = "df"	#database password (mabeh an hased value 4 later??)


## DHCP-server
class dhcp:
    leasefile = "/var/lib/dhcp/dhcpd.leases"
    

## Filters used in the firewall.
#  Don't mess with this, unless you REALLY KNOW what you are doing.
#  

class filter:
    ipv4_in_leasefile = r'([\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3})'
    mac_in_leasefile = r'([a-f|0-9][a-f|0-9]\:[a-f|0-9][a-f|0-9]\:[a-f|0-9][a-f|0-9]\:[a-f|0-9][a-f|0-9]\:[a-f|0-9][a-f|0-9]\:[a-f|0-9][a-f|0-9])'
    mac_exact = '';
    ip_exact = r'(^[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}$)'

