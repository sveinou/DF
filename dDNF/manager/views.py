from DNF import conf
from DNF.auth.drop import Drop
from DNF.firewall.firewall import Firewall
from dDNF.login.models import LoggedInUser
from dDNF.manager.forms import FirewallRule
from dDNF.manager.models import Rule
from django.contrib.sessions.models import Session
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
import logging
log = logging.getLogger(__name__)
log.addHandler(conf.log.web)
#log.addFilter(conf.log.logformat)
log.setLevel(conf.log.level)

def list_active(request, action=None):
    if request.user.is_anonymous() or not request.user.is_staff:
        return redirect('/')
    
    f = Firewall()
    error = False
    user = None
    try:
        if action and action == 'limit' and request.POST:
            user = LoggedInUser.objects.get(last_seen_ip=request.POST.get('victim'))        
            limit = request.POST.get('setlimit')
            if user:
                if limit == 'TX':
                    f.limit_tx(user.last_seen_ip)
                elif limit == 'RX':
                    f.limit_rx(user.last_seen_ip)
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
                [s.delete() for s in Session.objects.all() if s.get_decoded().get('_auth_user_id') == user.id]     
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
        limited += [LoggedInUser.objects.get(last_seen_ip=user[-2]) for user in f.get_limited() if user[-2] != '0.0.0.0/0' and user[2] != 'CONNLIMIT']
        
    except LoggedInUser.DoesNotExist:
        return render_to_response('active_users.html', {'limited':None, 'active':None, 'user':None, 'error':True, 'action':None}, context_instance=RequestContext(request))
    
    return render_to_response('active_users.html', {'limited':limited, 'active':allowed, 'user':user, 'error':error, 'action':action}, context_instance=RequestContext(request))    


def firewall(request, action):
    if request.user.is_anonymous() or not request.user.is_staff:
        return redirect('/')
        log.info("detected anon-user in adminpanel. Thrown out...")
    result = ''
    rules_form = FirewallRule()
    f = Firewall()
    log.debug('inside manager.views.firewall()')
    if action == 'add' and request.method == 'POST':
        log.debug('-- DETECTED ADD-RULE')
        form = FirewallRule(request.POST)
        rule = Rule()
        if form.is_valid():
            log.debug ('-- -- form is valid')
            rule.src = form.cleaned_data.get('src_ip')
            rule.src += '/' + str(form.cleaned_data.get('src_subnet'))
            rule.spt = form.cleaned_data.get('src_port')
            rule.dst = form.cleaned_data.get('dst_ip')
            if rule.dst: rule.dst += '/' + str(form.cleaned_data.get('dst_subnet'))
            rule.dpt = form.cleaned_data.get('dst_port')
            rule.action = form.cleaned_data.get('action')
            rule.chain = form.cleaned_data.get('chain') 
            rule.prot = form.cleaned_data.get('protocol')
            rule.save()
            log.debug('-- -- rule saved to db, sending rule to firewall.add_custom_rule')
            result = f.add_custom_rule(rule.chain, rule.src, rule.spt, rule.dst, rule.dpt, rule.action, rule.prot)
        rules_form = form;
    elif action == 'delete' and request.method == 'POST':
        log.debug('-- DETECTED DELETE-RULE')
        rule = str(request.POST.get('ruleid'))
        chain = str(request.POST.get('chain'))
        f.del_custom_rule(chain, rule);
    elif action == 'flush' and request.method == 'POST':
        log.debug('-- DETECTED FLUSH')
        chain = request.POST.get('chain')
        f.flush_custom_rules(chain)
        
    return render_to_response('firewall.html', {'result':result, 'forward':f.get_custom_forward(), 'input':f.get_custom_input(), 'form':rules_form}, context_instance=RequestContext(request))

def users(request):
    if request.user.is_anonymous() or not request.user.is_staff:
        return redirect('/')
    users = LoggedInUser.objects.all()
    pass


def show(request):
    if request.user.is_anonymous() or not request.user.is_staff:
        return redirect('/')
    
    return render_to_response('admin_home.html',{'conf':conf,}, context_instance=RequestContext(request))
    
