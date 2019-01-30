from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from spacextickets.accounts.models import User


# City
def validate_city_unique_in_state(city, exclude=None):
    from .models import City
    if City.objects.filter(name=city.name, state_id=city.state_id).exclude(id=city.id).count() > 0:
        raise ValidationError(_("There's already another city named like that in that state."))


# ScheduledTrip
def validate_schedtrip_duration(duration):
    if duration.total_seconds() <= 0:
        raise ValidationError(_("The trip's duration must be positive. We can't travel back in time (not yet!)."))


def validate_schedtrip_seats(seats):
    if seats <= 0:
        raise ValidationError(_("There must be at least one seat."))


def validate_schedtrip_price(price):
    if price <= 0:
        raise ValidationError(_("Trip's price must be positive."))


def validate_schedtrip(trip):
    if trip.departure_id == trip.arrival_id:
        raise ValidationError(_("Departing city can't be the same as the arrival one."))


def validate_schedtrip_unique(trip, exclude=None):
    from .models import ScheduledTrip
    clones = ScheduledTrip.objects.filter(departure=trip.departure, arrival=trip.arrival,
                                          week_day=trip.week_day, time=trip.time)
    if clones.exclude(id=trip.id).count() > 0:
        raise ValidationError(_("There's another trip scheduled identical to the one you are trying to add."))


# Order
def validate_order_user(user):
    user_obj = User.objects.get(id=user)
    if user_obj.is_staff:
        raise ValidationError(_("Staff accounts can't book a trip."))
    if not user_obj.is_active:
        raise ValidationError(_("User must be active to be able to book a trip."))


# Ticket
def validate_ticket_date(date):
    if date < timezone.now().date():
        raise ValidationError(_("Can't book a trip back in the past."))

