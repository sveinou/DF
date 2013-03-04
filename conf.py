

# global

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

## Filters used in the firewall.
#  Don't mess with this, unless you REALLY KNOW what you are doing.
#  

class filter:
    ipv4_in_leasefile = r'([\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3})'
    mac_in_leasefile = r'([a-f|0-9][a-f|0-9]\:[a-f|0-9][a-f|0-9]\:[a-f|0-9][a-f|0-9]\:[a-f|0-9][a-f|0-9]\:[a-f|0-9][a-f|0-9]\:[a-f|0-9][a-f|0-9])'
    mac_exact = '';
    ipv4_exact = r'(^[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}$)'


class exit_status:
    login_error = 1
    ip_mac_mismatch_error = 2
    input_error = 3
    other_exception = 9

