'''
Created on 19 Apr 2013

@author: espen
'''
from DNF.auth.login import Login
from django.contrib.auth.models import User

class FirstLoginAuth(object):
    '''
    Authenticate to DNF.auth.login, and add user to DJANGO userdb.
    '''
    
    def authenticate(self, username=None, password=None, ipaddress=None):
        "Saves user to django DB."
    
        if not username or not password or not ipaddress:
            return None
        
        login_ok = Login().ip4(username, password, ipaddress)
        if login_ok:
            try:
                user = User.objects.get(username=username)
                if not user.check_password(password):       #UPDATE PASSWORD IF CHANGED
                    user.set_password(password)
            except User.DoesNotExist:
                user = User(username=username)
                user.set_password(password)
                user.is_active = True
                user.is_staff = False
                user.is_superuser = False
                user.save()
            return user
            
        return None

        
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None