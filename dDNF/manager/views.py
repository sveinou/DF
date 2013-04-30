

from dDNF.manager.forms import FirewallRule
from dDNF.manager.models import Rule
from dDNF.login.models import LoggedInUser
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from DNF.firewall.firewall import Firewall
from DNF.auth.drop import Drop
from DNF import conf


# def edit_user(request):
#     if request.method == 'POST':
#         #form = UserForm(request.POST)
#         form = ""
#         if form.is_valid():
#             data = form.cleaned_data
#             user = LoggedInUser.objects.get(username=data['username'])
#             user.first_name = data['firstname']
#             user.last_name = data['lastname']
#             user.is_active = data['restrict']
#             user.save()
#             return HttpResponseRedirect('/admin/')
# 
# def blockuser(request):
#     pass

def list_active(request, action=None):
    if request.user.is_anonymous() or not request.user.is_staff:
        return redirect('/')
    
    f = Firewall()
    error = False
    user = None
    
    if action and action == 'limit' and request.POST:
        user = LoggedInUser.objects.get(last_seen_ip=request.POST.get('victim'))        
        limit = request.POST.get('setlimit')
        if user:
            if limit == 'TX':
                f.limit_tx(user.last_seen_ip)
            elif limit == 'RX':
                f.limit_tx(user.last_seen_ip)
            elif limit == 'C':
                f.limit_connections(user.last_seen_ip)
#            user.is_active = False
            else:
                error = True
        else:
            error = True

    elif action and action == 'kick' and request.POST:
        user = LoggedInUser.objects.get(last_seen_ip=request.POST.get('victim'))
        if user:
            Drop().ip4(user.last_seen_ip)
#            f.drop_ip4(user.last_seen_ip)
#            user.is_active = False        
        else:
            error = True;
        
    elif action and action == 'free' and request.POST:
        user = LoggedInUser.objects.get(last_seen_ip=request.POST.get('victim'))
        if user:
            user.is_active = True
            f.rm_limit(user.last_seen_ip)
        else:
            error = True

    allowed = [LoggedInUser.objects.get(last_seen_ip=user[-1]) for user in f.get_allowed() if user[-1] != '0.0.0.0/0']
    limited = [LoggedInUser.objects.get(last_seen_ip=user[-1]) for user in f.get_limited() if user[-1] != '0.0.0.0/0']
        
    return render_to_response('active_users.html', {'limited':limited, 'active':allowed, 'user':user, 'error':error, 'action':action}, context_instance=RequestContext(request))    


def firewall(request):
    if request.user.is_anonymous() or not request.user.is_staff:
        return redirect('/')
    f = Firewall()
    if request.method == 'POST':
        form = FirewallRule(request.POST)
        rule = Rule()
        if form.is_valid():
            rule.src = str(form['src_ip']+'/'+form['src_subnet'])
            rule.spt = str(form['src_port'])
            rule.dst = str(form['dst_ip']+'/'+form['dst_subnet'])
            rule.dpt = str(form['dst_port'])
            rule.action = str(form['action'])
            rule.chain = str(form['chain']) 
            
            
            "iptables -I CUSTOM_chain -s src --sport spt -d dst --dport dpt -j action"
            
    rules_form = FirewallRule()
    
    
    return render_to_response('firewall.html', {'forward':f.get_custom_forward(), 'input':f.get_custom_input(), 'form':newform}, context_instance=RequestContext(request))

def users(request):
    if request.user.is_anonymous() or not request.user.is_staff:
        return redirect('/')
    users = LoggedInUser.objects.all()
    pass


def show(request):
    if request.user.is_anonymous() or not request.user.is_staff:
        return redirect('/')
    
    return render_to_response('admin_home.html',{'conf':conf,}, context_instance=RequestContext(request))
    