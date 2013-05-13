'''
Created on 19 Apr 2013

@author: espen
'''
from DNF.auth.login import Login
from dDNF.login.models import LoggedInUser
from django.contrib.auth.models import User
import logging

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
                user = LoggedInUser.objects.get(username=username)
                user.last_seen_ip = ipaddress
                if not user.check_password(password):       #UPDATE PASSWORD IF CHANGED
                    user.set_password(password)
                user.save()
            except LoggedInUser.DoesNotExist:
                user = LoggedInUser(username=username)
                user.set_password(password)
                user.is_active = True
                user.is_staff = False
                user.is_superuser = False
                user.last_seen_ip = ipaddress
                user.save()
            return user
            
        return None

        
    def get_user(self, user_id):
        try:
            return LoggedInUser.objects.get(pk=user_id)
        except LoggedInUser.DoesNotExist:
            return None
        
from DNF.stats.info import Dhcp 
from DNF import conf
from DNF.firewall.firewall import Firewall
from DNF.database.df_data import Data

class DjangoDBLogin(object):
    '''
    Login using DJANGO-userdatabase
    '''
    log = logging.getLogger(__name__)
    log.addHandler(conf.log.users)
    log.setLevel(conf.log.level)
    
    
    def authenticate(self, username=None, password=None, ipaddress=None):    
        self.log.debug("Trying login with DjangoDBLogin")
        if not username or not password or not ipaddress:
            self.log.debug("DjangoDBLogin not satisfied.")
            return None
        
        mac = Dhcp().find_mac(ipaddress) 
        self.log.info("trying to login %s@%s with mac: %s, " % (username, ipaddress, mac))
        
        if mac:
            self.log.debug("Mac OK.. getting user.")
            try:
                user = LoggedInUser.objects.get(username=username)
                if user.check_password(password):
                    user.last_seen_ip = ipaddress
                    self.log.debug("Found user, updating and logging in.")
                    self._openfw(ipaddress, username, mac)
                    return user
                else:
                    self.log.debug("Found user, but check_password failed.")
                    return None
            except LoggedInUser.DoesNotExist:
                try:
                    user = User.objects.get(username=username)
                    self.log.debug("User exists as djangoauth-user")
                    if user.check_password(password):
                        newuser = LoggedInUser(username=user.username)
                        newuser.set_password(password)
                        newuser.is_active = user.is_active
                        newuser.is_staff = user.is_staff
                        newuser.is_superuser =  user.is_superuser
                        newuser.last_seen_ip = ipaddress
                        user.delete()
                        newuser.save()
                        self.log.debug("user migrated to LoggedInUser and deleted from native db")
                        self._openfw(ipaddress, username, mac)
                        return newuser;
                    else:
                        self.log.debug(".. but password is wrong.")
                except User.DoesNotExist:
                    self.log.info("user %s does not exist." % (username))
                    return None
        else:
            self.log.debug("Could not find MAC for %s" % (ipaddress))
            return None
    
    def _openfw(self, ip, user, mac):
        f = Firewall()
        d = Data()
        f.accept_ip4(ip)
        d.mark_user_active(user, mac, ip)
    
    def get_user(self, user_id):
        try:
            return LoggedInUser.objects.get(pk=user_id)
        except LoggedInUser.DoesNotExist:
            return None