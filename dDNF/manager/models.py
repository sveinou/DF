from django.db import models

# class InterfaceTypes(models.Model):
#     name = models.CharField(max_length=24)
# 
# class Interface(models.Model):
#     name = models.CharField(max_length=24)
#     address = models.IPAddressField()
#     type = models.OneToOneField(InterfaceTypes)
#     
# 
# class FirewallRule():
#     name = models.CharField(max_length=24)
#     
# class Settings(models.Model):
#     ext_if = models.OneToOneField(Interface.sett)
#     int_if = models.OneToOneField(Interface.sett)

class Rule(models.Model):
    chain = models.CharField(max_length=7) #FORWARD / INPUT
    prot = models.CharField(max_length=3, null=True) #TCP/UDP/null 
    src = models.CharField(max_length=20)
    spt = models.CharField(max_length=5, null=True)
    dst = models.CharField(max_length=20, null=True)
    dpt = models.CharField(max_length=5, null=True)
    action = models.CharField(max_length=6) #DROP / ACCEPT / REJECT 
