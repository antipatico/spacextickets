from django.contrib.admin import register, ModelAdmin
from .models import *


@register(Ticket)
class TicketAdmin(ModelAdmin):
    search_fields = ['ticket_code', ]
    list_display = ('ticket_code', 'order', 'traveler', 'trip', 'date')


@register(Order)
class OrderAdmin(ModelAdmin):
    search_fields = ['booking_code']
    list_display = ('user', 'order_date', 'is_temporary')
