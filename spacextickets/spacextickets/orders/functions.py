import json

from django.db.models.query import EmptyQuerySet

from spacextickets.accounts.models import Traveler
from spacextickets.orders.models import Order, Ticket
from spacextickets.utils.json import UUIDDecoder


def delete_order(order_pk, is_temporary=True):
    try:
        order = Order.objects.get(pk=order_pk, is_temporary=is_temporary)
        user = order.user
        try:
            tickets = Ticket.objects.filter(order=order)
        except Ticket.DoesNotExist:
            tickets = EmptyQuerySet()
        travelers = tickets.values_list('traveler', flat=True).distinct()
        if user and user.is_guest():
            for traveler_pk in travelers:
                try:
                    Traveler.objects.get(pk=traveler_pk).delete()
                except Traveler.DoesNotExist:
                    pass
        for ticket in tickets:
            ticket.delete()
        if user and user.is_guest():
            user.delete()
        order.delete()
    except Order.DoesNotExist:
        pass


def delete_session_order(request):
    if "order" in request.session:
        order_pk = json.loads(request.session['order'], cls=UUIDDecoder)
        delete_order(order_pk)
        del request.session['order']
        request.session.save()
