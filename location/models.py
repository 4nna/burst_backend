from math import *

from django.db import models


# Create your models here.
class Location(models.Model):
    longtitude = models.FloatField(verbose_name='Longtitude')
    latitude = models.FloatField(verbose_name='Latitude')


CENTER = Location(longtitude=15, latitude=15)
RADIUS = 2  # km


def distance(first_location: Location, second_location: Location):
    other_location = first_location
    this_location = second_location

    longitude_diff = abs(this_location.longtitude - other_location.longtitude)
    latidude_diff = abs(this_location.latitude - other_location.latitude)

    earth_radius = 6373.0

    a = sin(latidude_diff / 2) ** 2 + \
        cos(this_location.latitude) * \
        cos(other_location.latitude) * \
        sin(longitude_diff / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = earth_radius * c

    return distance
