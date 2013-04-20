from django.conf.urls.defaults import *
from django.conf import settings
from dDNF.login.views import checkmeta, dnf_login, dnf_logout
from dDNF.statistics.views import user_stats
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^meta/$', checkmeta),    
    (r'^stats/$', user_stats),
    (r'/logout/$', dnf_logout),
    (r'^gfx/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.STATIC_DOC_ROOT}), 
    ('^media/(?P<path>.*)$','django.views.static.serve', {'document_root':settings.ADMIN_DOC_ROOT}),
    # (r'^dDNF/', include('dDNF.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     (r'^admin/user/', include(admin.site.urls)),
     (r'^', dnf_login)
)
#if settings.DEBUG: 
#        urlpatterns += patterns( 
#       (r'^media/(?P<path>.*)$', 'django.views.static.serve', 
#{'document_root':'./media/'}), 
#    ) 
