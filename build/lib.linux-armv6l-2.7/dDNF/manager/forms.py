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
    wgt_ip = forms.TextInput(attrs={'size':15})
    protocol = forms.ChoiceField(choices=[('None','None'),('TCP','TCP'),('UDP','UDP')], label='Proto',required=False,help_text='Protocol to be used. TCP or UDP. You must set ports if you are using this setting.')
    src_ip = forms.IPAddressField(label='Source IP', widget=wgt_ip, help_text='The IP-address of the source of packet.')
    src_subnet = forms.IntegerField(min_value=0, max_value=32, widget=wgt_sub, label='mask', help_text='Network mask of Source IP-address.')
    src_port = forms.IntegerField(min_value=0, max_value=65535, label='Port', widget=wgt_port, required=False, help_text='Source Port of packet')
    dst_ip = forms.IPAddressField(label='Destination IP', required=False, widget=wgt_ip, help_text='Destination IP-address of packet')
    dst_port = forms.IntegerField(min_value=0, max_value=65535, label='Port', widget=wgt_port, required=False, help_text='Destination port of incoming packet.')
    dst_subnet = forms.IntegerField(min_value=0, max_value=32, widget=wgt_sub, label='mask', help_text='Network mask of Destination IP-address')
    action = forms.ChoiceField(choices=[('DROP','DROP'),('ACCEPT','ACCEPT'),('REJECT','REJECT')], label='Target', help_text="What to do with matching packets")
    chain = forms.ChoiceField(choices=[('FORWARD','FORWARD'),('INPUT','INPUT')], label='Chain', help_text='Which kind of traffic the rule should apply to.')

    def clean(self):
        clean = super(FirewallRule, self).clean()
        
        proto = clean.get('protocol')
        dst = clean.get('dst_port')
        src = clean.get('src_port')
        
        if proto == 'None':
            msg = u"Set protocol"
            if dst:
                self._errors['dst_port'] = self.error_class([msg])
            if src:
                self._errors['src_port'] = self.error_class([msg])
            if src or dst:
                self._errors['protocol'] = self.error_class([u"Protocol must be set when using ports"])
        
        return clean

            