# Create your views here.
from django.http import HttpResponse
from DNF.auth.login import Login
from DNF.auth.drop import Drop
from DNF.stats import info 
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.template import RequestContext
#from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
l = Login()
d = Drop()
ip = info.IP()

@csrf_protect
def dnf_login(request):    
    ip_addr = str(request.META['REMOTE_ADDR'])
    if ip.isLoggedIn(ip_addr):# and request.user.is_authenticated():        
        return redirect('/stats/')
    
    if not request.POST:
        link = "http://"+request.META.get('HTTP_HOST')+request.get_full_path()
        return render_to_response("login.html",{'link':link}, context_instance=RequestContext(request))
    else:
        username = request.POST['username'].encode('utf-8')
        password = request.POST['password'].encode('utf-8')
        
        if request.POST['link']:
            link = str(request.POST['link'])
        else:
            link = "/"
        
        if not username or not password:
            return render_to_response("login.html",{'link':link,'no_post':True}, context_instance=RequestContext(request))
            
        user = authenticate(username=username, password=password, ipaddress=ip_addr)       
        if user and user.is_active:
            login(request, user)
            return redirect(link)
        elif user and not user.is_active:
            d.ip(ip_addr)
            return render_to_response('login.html',{'deactivated':True}, context_instance=RequestContext(request))
        else:
            return render_to_response('login.html',{'link':link, 'failed':True}, context_instance=RequestContext(request))
         
    return render_to_response("login.html",{'no_post':True}, context_instance=RequestContext(request))

def dnf_logout(request):
    ip_addr = str(request.META['REMOTE_ADDR'])
    d.ip4(ip_addr)
    logout(request)
    return render_to_response('login.html',{'logout':True})

def checkmeta(request):
    values = request.META.items()
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>M: %s</td><td>%s</td></tr>' % (k, v))
    values = request.GET.items()
    values.sort()    
    for k, v in values:
        html.append('<tr><td>G: %s</td><td>%s</td></tr>' % (k, v))    
    return HttpResponse('<table>%s</table>' % '\n'.join(html))