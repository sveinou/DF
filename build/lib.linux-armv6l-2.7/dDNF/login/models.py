from django.contrib.auth.models import User
from django.db import models

class LoggedInUser(User):
    last_seen_ip = models.IPAddressField()