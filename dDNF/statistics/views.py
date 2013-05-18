# Create your views here.

from DNF import conf
from DNF.stats.info import Statistics, IP 
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
stats = Statistics()

def user_stats(request):
    ipaddr = request.META.get('REMOTE_ADDR')
    if not IP().isLoggedIn(ipaddr):
        return redirect('/')
        
    #ipaddr = request.META['REMOTE_ADDR']
    conn = [c.split() for c in stats.get_connections(ipaddr)]       #lag liste m list
    conn_clean = [(str(c[0])+ ' ' + str(c[3:9])) for c in conn if c]     #lag liste m tekst
    conn = conn_clean
    io = stats.get_iptables_io(ipaddr)
    limited = stats.is_limited(ipaddr)
    limit = [conf.bandwidth.max_connections,conf.bandwidth.max_rxs,conf.bandwidth.max_txs]
    intip = (conf.internal_network).split('/')[0]
    server = 'http://%s' % (intip)
    
    return render_to_response('stats.html',{'server':server, 'ip':ipaddr,'io':io,'conn':conn, 'user':request.user, 'limited': limited, 'limit':limit[0]}, context_instance=RequestContext(request))

    
