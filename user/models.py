from django.contrib.auth.models import AbstractUser
from django.db import models

from location.models import Location


class User(AbstractUser):
    name = models.CharField(max_length=100, blank=True, null=True)
    matchable = models.BooleanField(default=False)
    current_location = models.OneToOneField(Location,
                                            on_delete=models.CASCADE,
                                            default=None, null=True,
                                            blank=True)

    def __str__(self):
        return self.username
