from django.test import TestCase
from spacextickets.accounts.models import *
from spacextickets.core.models import *
from .functions import *
from django.utils import timezone


class TestOrderDelete(TestCase):
    def test_order_deleted(self):
        order = Order()
        order.save()
        delete_order(order_pk=order.pk)

        self.assertEqual(Order.objects.filter(booking_code=order.pk).exists(), False)

    def test_tickets_deleted(self):
        order = Order()
        trip = ScheduledTrip()
        order.save()
        for i in range(0, 5):
            t = Ticket(order_id=order.pk, date=timezone.now(), trip=trip)
            t.save()

        delete_order(order_pk=order.pk)
        self.assertEqual(Ticket.objects.filter(order_id=order.pk).exists(), False)

    def test_guestUser_deleted(self):
        user = GuestUser(first_name="Mario", last_name="Rossi", gender="M", email="mario@rossi")
        user.save()
        order = Order(user=user)
        order.save()

        delete_order(order_pk=order.pk)
        self.assertEqual(GuestUser.objects.filter(id=user.id).exists(), False)

    def test_traveler_deleted_if_guest(self):
        user = GuestUser(first_name="Mario", last_name="Rossi", gender="M", email="mario@rossi")
        user.save()

        s = State(name="Italy")
        s.save()

        t = Traveler(user=user, birthday=timezone.now(), state=s, first_name="Paolo")
        t.save()

        order = Order(user=user)
        order.save()

        trip = ScheduledTrip()
        ti = Ticket(order_id=order.pk, date=timezone.now(), trip=trip, traveler=t)
        ti.save()

        delete_order(order_pk=order.pk)

        self.assertEqual(Traveler.objects.filter(id=t.id).exists(), False)

    def test_traveler_not_deleted_if_user(self):
        user = User(first_name="Mario", last_name="Rossi", gender="M", email="mario@rossi")
        user.save()
        s = State(name="Italy")
        s.save()
        t = Traveler(user=user, birthday=timezone.now(), state=s)
        t.save()

        order = Order(user=user)
        order.save()

        trip = ScheduledTrip()
        ti = Ticket(order_id=order.pk, date=timezone.now(), trip=trip, traveler_id=t.id)
        ti.save()

        delete_order(order_pk=order.pk)

        self.assertEqual(Traveler.objects.filter(id=t.id).exists(), True)