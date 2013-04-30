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
    wgt_port = forms.TextInput(attrs={'size': 5}) 
    wgt_sub = forms.TextInput(attrs={'size': 2, 'value':32})
    src_ip = forms.IPAddressField(label='Source IP')
    src_subnet = forms.IntegerField(min_value=0, max_value=32, widget=wgt_sub)
    src_port = forms.IntegerField(min_value=0, max_value=65535, label='Source Port', widget=wgt_port)
    dst_ip = forms.IPAddressField(label='Destination IP')
    dst_port = forms.IntegerField(min_value=0, max_value=65535, label='Destination Post', widget=wgt_port)
    dst_subnet = forms.IntegerField(min_value=0, max_value=32, widget=wgt_sub)
    action = forms.ChoiceField(choices=[('ACCEPT','ACCEPT'),('DROP','DROP'),('REJECT','REJECT')], label='Action')
    chain = forms.ChoiceField(choices=[('FORWARD','FORWARD'),('INPUT','INPUT')], label='Chain')