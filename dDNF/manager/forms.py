'''
Created on 21 Apr 2013

@author: espen
'''
from django import forms

class NetworkSettings(forms.Form):
    ext_ip = forms.IPAddressField(label='External IP')
    int_ip = forms.IPAddressField(label='Internal IP')
    int_if = forms.CharField(label='Internal Interface')
    ext_if = forms.CharField(label='External Interface')
    
class FirewallRule(forms.Form):
    rule = forms.CharField(label='IPTABLES RULE')
    