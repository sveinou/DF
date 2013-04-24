from django.conf.urls.defaults import *
from django.conf import settings
from dDNF.login.views import checkmeta, dnf_login, dnf_logout
from dDNF.statistics.views import user_stats
from dDNF.manager.views import show, list_active, firewall
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^meta/$', checkmeta),    
    (r'^stats/$', user_stats),
    (r'/logout/$', dnf_logout),

# MEDIA-stuff    
    (r'^gfx/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.STATIC_DOC_ROOT}), 
    ('^media/(?P<path>.*)$','django.views.static.serve', {'document_root':settings.ADMIN_DOC_ROOT}),

# ADMIN STUFF    
     (r'^admin/$', show),
     (r'^admin/currently-active/$', list_active),
     (r'^admin/firewall/$', firewall),
     (r'^admin/user/', include(admin.site.urls)),

## CATCH-ALL
     (r'^', dnf_login)
)
#if settings.DEBUG: 
#        urlpatterns += patterns( 
#       (r'^media/(?P<path>.*)$', 'django.views.static.serve', 
#{'document_root':'./media/'}), 
#    ) 
