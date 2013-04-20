# Create your views here.

from DNF.stats.info import Statistics 
from DNF import conf
from django.shortcuts import render_to_response, redirect
#from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
stats = Statistics()

#@login_required(login_url='/stats/')
def user_stats(request):
    user = request.user;

    if user.is_authenticated():
        ipaddr = request.META['REMOTE_ADDR']
        conn = stats.get_connections(ipaddr)
        io = stats.get_iptables_io(ipaddr)
        limited = stats.is_limited(ipaddr)
        limit = [conf.bandwidth.max_connections,conf.bandwidth.max_rxs,conf.bandwidth.max_txs]
        return render_to_response('stats.html',{'ip':ipaddr,'io':io,'conn':conn, 'user':user, 'limited': limited, 'limit':limit[0]})
    
    logout(request)
    return redirect('/')
    