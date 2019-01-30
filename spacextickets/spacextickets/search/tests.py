from django.shortcuts import reverse
from django.test import TestCase
from django.utils import timezone
from spacextickets.core.models import *
import datetime


class TestSearchView(TestCase):
    dep = None
    arr = None

    def populate_db(self):
        Italy = State.objects.create(name="Italy", continent="EU")
        self.dep = City.objects.create(name="test_dep", state=Italy)
        self.arr = City.objects.create(name="test_ret", state=Italy)

        for wd in range(0, 7):
            ScheduledTrip.objects.create(departure=self.dep, arrival=self.arr, week_day=wd, time="23:00:00",
                                         duration=datetime.timedelta(hours=1), price=12312.321)
            ScheduledTrip.objects.create(departure=self.arr, arrival=self.dep, week_day=wd, time="23:00:00",
                                         duration=datetime.timedelta(hours=1), price=12312.321)

    def test_no_results(self):
        self.populate_db()

        # Departure and arrival station are not in the db
        data = {'departure': "XXX", 'arrival': "YYY",
                'dep_date': (timezone.now() + datetime.timedelta(days=1)).date(),
                'dep_time': (timezone.now() + datetime.timedelta(hours=1)).time(),
                'seats': 1}

        response = self.client.post(reverse("search:search"), data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No trips found")

    def test_no_results_wrong_ret_date(self):
        self.populate_db()

        # Return date smaller than departure date
        data = {'departure': self.dep, 'arrival': self.arr,
                'dep_date': (timezone.now() + datetime.timedelta(days=3)).date(),
                'dep_time': (timezone.now() + datetime.timedelta(hours=1)).time(),
                'ret_date': (timezone.now() - datetime.timedelta(days=3)).date(),
                'ret_time': (timezone.now() - datetime.timedelta(hours=1)).time(),
                'seats': 1}
        response = self.client.post(reverse("search:search"), data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No trips found")

    def test_no_results_wrong_dep_date(self):
        self.populate_db()

        # Departure date smaller than timezone.now()
        data = {'departure': self.dep, 'arrival': self.arr,
                'dep_date': (timezone.now() - datetime.timedelta(days=5)).date(),
                'dep_time': (timezone.now() + datetime.timedelta(hours=1)).time(),
                'seats': 1}
        response = self.client.post(reverse("search:search"), data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No trips found")

    def test_no_results_wrong_time(self):
        self.populate_db()

        # Departure date smaller than timezone.now()
        data = {'departure': self.dep, 'arrival': self.arr,
                'dep_date': (timezone.now()).date(),
                'dep_time': (timezone.now() - datetime.timedelta(hours=1)).time(),
                'seats': 1}
        response = self.client.post(reverse("search:search"), data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No trips found")

    def test_no_results_zero_seats(self):
        self.populate_db()

        # Zero Seats
        data = {'departure': self.dep, 'arrival': self.arr,
                'dep_date': (timezone.now() + datetime.timedelta(days=1)).date(),
                'dep_time': (timezone.now() + datetime.timedelta(hours=1)).time(),
                'seats': 0}
        response = self.client.post(reverse("search:search"), data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No trips found")

    def test_search_get(self):
        response = self.client.get(reverse("search:search"))
        self.assertEqual(response.status_code, 302)

    def test_search_post(self):
        response = self.client.post(reverse("search:search"))
        self.assertEqual(response.status_code, 200)
