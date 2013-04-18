from django.conf.urls.defaults import *
from django.conf import settings
from login.views import checkmeta, login, logout
from statistics.views import user_stats
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^meta/$', checkmeta),    
    (r'^stats/$', user_stats),
    (r'/logout/$', logout),
    (r'^gfx/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.STATIC_DOC_ROOT}), 
    (r'^', login),
    # (r'^dDNF/', include('dDNF.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
#if settings.DEBUG: 
#        urlpatterns += patterns( 
#       (r'^media/(?P<path>.*)$', 'django.views.static.serve', 
#{'document_root':'./media/'}), 
#    ) 
