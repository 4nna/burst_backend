from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser

from location.models import Location


class User(AbstractUser):
    name = models.CharField(max_length=100, blank=True, null=True)
    matchable = models.BooleanField(default=False)
    current_location = Location