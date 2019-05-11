from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser

from location.models import Location

from math import sin, cos, sqrt, atan2, radians


class User(AbstractUser):
    name = models.CharField(max_length=100, blank=True, null=True)
    matchable = models.BooleanField(default=False)
    current_location = models.OneToOneField(Location,
                                            on_delete=models.CASCADE,
                                            default=None, null=True,
                                            blank=True)

    def get_distance(self, User):
        other_location = User.current_location
        this_location = self.current_location

        longitude_diff = abs(this_location.longtitude - other_location.longtitude)
        latidude_diff = abs(this_location.latitude - other_location.latitude)

        earth_radius = 6373.0

        a = sin(latidude_diff / 2)**2 + cos(this_location.latitude) * cos(other_location.latitude) * sin(longitude_diff
                                                                                                         / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = earth_radius * c

        return distance
