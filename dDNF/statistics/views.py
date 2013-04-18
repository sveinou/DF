# Create your views here.
from django.http import HttpResponse
from DNF.stats.info import Statistics 
from DNF import conf
from django.shortcuts import render_to_response, redirect

stats = Statistics()


def user_stats(request):
    ipaddr = request.META['REMOTE_ADDR']
    #conn = stats.get_conntrack(ipaddr)
    conn = stats.get_connections(ipaddr)
    io = stats.get_iptables_io(ipaddr)
    limited = stats.is_limited(ipaddr)
    limit = [conf.bandwidth.max_connections,conf.bandwidth.max_rxs,conf.bandwidth.max_txs]
    
    return render_to_response('stats.html',{'ip':ipaddr,'io':io,'conn':conn, 'limited': limited, 'limit':limit[0]})
    