from django.utils import timezone

from spacextickets.core.models import ScheduledTrip
from spacextickets.orders.models import Ticket


def search_trips(departure, arrival, date, time, seats, langcode):
    ret_trips = []
    kwargs = {'departure__name_%s__iexact' % langcode: departure,
              'arrival__name_%s__iexact' % langcode: arrival}

    trips = ScheduledTrip.objects.all().filter(week_day=date.weekday(), **kwargs)
    if timezone.now().date() == date:
        trips = trips.filter(time__gt=timezone.now().time())
    if time:
        trips = trips.filter(time__gte=time)

    for trip in trips:
        available_seats = trip.seats - Ticket.objects.filter(trip_id=trip.id).count()
        if available_seats >= seats:
            ret_trips += [(trip, available_seats)]

    return ret_trips
