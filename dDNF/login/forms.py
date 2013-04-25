'''
Created on 24 Apr 2013

@author: espen
'''
from django import forms
from dDNF.login.models import LoggedInUser

class LoggedInUserRegistrationForm(forms.ModelForm):
    class Meta:
        model = LoggedInUser
        fields = ('username','last_seen_ip','last_login')