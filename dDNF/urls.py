from django.conf.urls.defaults import *
from django.conf import settings
#from dDNF.login.views import checkmeta, dnf_login, dnf_logout
#from dDNF.statistics.views import user_stats
#from dDNF.manager.views import show, list_active, firewall
from dDNF import manager, statistics, login
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('dDNF.login.views',
                      (r'^meta/$', 'checkmeta'),
                      (r'/logout/$', 'dnf_logout'),
)
urlpatterns += patterns('dDNF.statistics.views',    
    (r'^stats/$', 'user_stats'),
)
# MEDIA-stuff    
urlpatterns += patterns('',
    (r'^gfx/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.STATIC_DOC_ROOT}), 
    ('^media/(?P<path>.*)$','django.views.static.serve', {'document_root':settings.ADMIN_DOC_ROOT}),
)
urlpatterns += patterns('dDNF.manager.views',
# ADMIN STUFF    
     (r'^admin/$', 'show'),
     (r'^admin/currently-active/$', 'list_active'),
     (r'^admin/currently-active/kick/$', 'list_active', {'action':'kick'}),
     (r'^admin/currently-active/limit/$', 'list_active', {'action':'limit'}),
     (r'^admin/currently-active/free/$', 'list_active', {'action':'free'}),
     (r'^admin/firewall/$', 'firewall',{'action':'show'}),
     (r'^admin/firewall/add/$', 'firewall',{'action':'add'}),
     (r'^admin/firewall/delete/$', 'firewall',{'action':'delete'}),
     (r'^admin/firewall/flush/$', 'firewall',{'action':'flush'}),
)

urlpatterns += patterns('',
     (r'^admin/user/', include(admin.site.urls)),
     (r'^', 'dDNF.login.views.dnf_login')
)
#if settings.DEBUG: 
#        urlpatterns += patterns( 
#       (r'^media/(?P<path>.*)$', 'django.views.static.serve', 
#{'document_root':'./media/'}), 
#    ) 
