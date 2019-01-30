from django.contrib.admin import register, ModelAdmin
from .models import *


@register(Marker)
class MarkerAdmin (ModelAdmin):
    search_fields = ['city']
    list_display = ['city', 'lat', 'long']
