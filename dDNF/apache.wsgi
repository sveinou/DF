'''
Created on 12 Apr 2013

@author: espen
'''

import os, sys
path = '/home/espen/workspace/combo/'

if path not in sys.path:
    sys.path.append(path)
    
os.environ['DJANGO_SETTINGS_MODULE'] = 'dDNF.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
