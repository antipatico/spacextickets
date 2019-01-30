from django.db import models
from spacextickets.accounts.models import BaseUser, Traveler
from spacextickets.core.models import ScheduledTrip
from spacextickets.core.validation import *
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
import uuid


class Order(models.Model):
    user = models.ForeignKey(BaseUser, null=True, validators=[validate_order_user], verbose_name=_('user'))
    order_date = models.DateTimeField(default=timezone.now, editable=False, verbose_name=_('order date'))
    booking_code = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, verbose_name=_('booking code'))
    is_temporary = models.BooleanField(default=True, verbose_name=_('temporary_order'))

    def __str__(self):
        return "Booking #%s" % str(self.booking_code)

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')


class Ticket(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name=_('order'))
    traveler = models.ForeignKey(Traveler, null=True, verbose_name=_('traveler'))
    trip = models.ForeignKey(ScheduledTrip, verbose_name=_('trip'))
    date = models.DateField(verbose_name=_('departing date'), validators=[validate_ticket_date])
    ticket_code = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name=_('ticket code'))

    def __str__(self):
        return "Ticket #%s" % str(self.ticket_code)

    class Meta:
        verbose_name = _('ticket')
        verbose_name_plural = _('tickets')
