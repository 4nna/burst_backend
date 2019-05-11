from django.db import models

from user.models import User
from location.models import Location

class Zone(models.Model):
    user_list = models.ForeignKey('User')
    radius = 500.0
    center = Location(longtitude=49.01, latitude=8.404)
