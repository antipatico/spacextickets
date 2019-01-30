from django.shortcuts import render

from spacextickets.core.models import ScheduledTrip
from .models import Marker


def show_maps(request):
    map_data = list()
    markers = Marker.objects.all()
    for marker in markers:
        destinations = list()
        cities = ScheduledTrip.objects.filter(departure=marker.city).values_list("arrival", flat=True).distinct()
        for city in cities:
            try:
                destinations.append(Marker.objects.get(city=city))
            except Marker.DoesNotExist:
                pass
        map_data.append((marker, destinations))

    return render(request=request, template_name="gmaps/maps.html", context={'map_data': map_data})
