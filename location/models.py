from django.db import models


# Create your models here.
class Location(models.Model):
    longtitude = models.FloatField(verbose_name='Longtitude')
    latitude = models.FloatField(verbose_name='Latitude')
