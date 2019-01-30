from django.db import models
from spacextickets.core.models import City


class Marker(models.Model):
    city = models.OneToOneField(City, primary_key=True, verbose_name='city')
    lat = models.FloatField(verbose_name='latitude')
    long = models.FloatField(verbose_name='longitude')
