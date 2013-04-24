

from dDNF.manager.forms import FirewallRule, NetworkSettings
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from DNF.firewall.firewall import Firewall

def edit_user(request):
    if request.method == 'POST':
        #form = UserForm(request.POST)
        form = ""
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.get(username=data['username'])
            user.first_name = data['firstname']
            user.last_name = data['lastname']
            user.is_active = data['restrict']
            user.save()
            return HttpResponseRedirect('/admin/')

def blockuser(request):
    pass

def list_active(request):
    f = Firewall()
    allowed = [user[-1] for user in f.get_allowed() if user[-1] != '0.0.0.0/0']
    limited = [user[-1] for user in f.get_limited() if user[-1] != '0.0.0.0/0']
    
            
    return render_to_response('active_users.html', {'limited':limited, 'active':allowed}, context_instance=RequestContext(request))
    
def firewall(request):
    f = Firewall()
    FORWARD = [{'j': fw[2], 'p':fw[3], 'i':fw[5], 'o':fw[6], 's':fw[7],'d':fw[8], 'rest':fw[9:]} for fw in f.get_custom_forward()]
    INPUT = [{'j': fw[2], 'p':fw[3], 'i':fw[5], 'o':fw[6], 's':fw[7],'d':fw[8], 'rest':fw[9:]} for fw in f.get_custom_input()]
    
    return render_to_response('firewall.html', {'forward':FORWARD, 'input':INPUT})
    

def show(request):
    users = User.objects.all()
    forms = {'firewall':FirewallRule(), 'network': NetworkSettings()}
    return render_to_response('admin_page.html', {'users':users, 'forms':forms}, context_instance=RequestContext(request))
