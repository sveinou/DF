'''
Created on 12 Apr 2013

@author: espen

Connects settings module and handler to mod_WSGI

'''

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'dDNF.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
