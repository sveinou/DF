from django.db import models

class InterfaceTypes(models.Model):
    name = models.CharField(max_length=24)

class Interface(models.Model):
    name = models.CharField(max_length=24)
    address = models.IPAddressField()
    type = models.OneToOneField(InterfaceTypes)

class FirewallRule():
    name = models.CharField(max_length=24)
    
class Settings(models.Model):
    ext_if = models.OneToOneField(Interface)
    int_if = models.OneToOneField(Interface)
    firewall_rules = models.ManyToOneRel(FirewallRule)  

