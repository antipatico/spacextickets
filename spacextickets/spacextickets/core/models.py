from django.db import models
from django.utils.datetime_safe import datetime
from django.utils.translation import ugettext_lazy as _
import uuid
from spacextickets.accounts.models import Traveler, BaseUser
from .validation import *

CONTINENT_CHOICES = (
    ('AF', _('Africa')),
    ('AN', _('Antarctica')),
    ('AS', _('Asia')),
    ('EU', _('Europe')),
    ('NA', _('North America')),
    ('SA', _('South America')),
    ('OC', _('Oceania')),
)

WEEK_DAY_CHOICES = (
    (0, _('Monday')),
    (1, _('Tuesday')),
    (2, _('Wednesday')),
    (3, _('Thursday')),
    (4, _('Friday')),
    (5, _('Saturday')),
    (6, _('Sunday')),
)


class State(models.Model):
    name = models.CharField(max_length=15, unique=True, verbose_name=_('name'))
    continent = models.CharField(max_length=2, choices=CONTINENT_CHOICES, verbose_name=_('continent'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('state')
        verbose_name_plural = _('states')


class City(models.Model):
    name = models.CharField(max_length=15, verbose_name=_('name'))
    state = models.ForeignKey(State, verbose_name=_("state"))

    validate_unique = validate_city_unique_in_state

    def __str__(self):
        return self.name

    def get_continent_display(self):
        return self.state.get_continent_display()

    class Meta:
        verbose_name = _('city')
        verbose_name_plural = _('cities')
        unique_together = (('name', 'state'),)


class ScheduledTrip(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    departure = models.ForeignKey(City, related_name='departure', verbose_name=_('departure'))
    arrival = models.ForeignKey(City, related_name='arrival', verbose_name=_('arrival'))
    week_day = models.PositiveSmallIntegerField(choices=WEEK_DAY_CHOICES, verbose_name=_('day of the week'))
    time = models.TimeField(verbose_name=_('departure time'), help_text=_("in UTC time"))
    duration = models.DurationField(validators=[validate_schedtrip_duration], verbose_name=_('duration'))
    seats = models.PositiveSmallIntegerField(default=3, validators=[validate_schedtrip_seats],
                                             verbose_name=_('seats'), help_text=_('maximum number'))
    price = models.DecimalField(max_digits=9, decimal_places=2, validators=[validate_schedtrip_price],
                                verbose_name=_('price'), help_text=_('in EUR'))

    clean = validate_schedtrip
    validate_unique = validate_schedtrip_unique

    def arrival_time(self):
        arrival_datetime = datetime.combine(datetime.today(), self.time) + self.duration
        return arrival_datetime.time()

    def __str__(self):
        return "%s ➔ %s" % (self.departure.name, self.arrival.name)

    class Meta:
        verbose_name = _('scheduled trip')
        verbose_name_plural = _('scheduled trips')
        unique_together = ('departure', 'arrival', 'week_day', 'time')
