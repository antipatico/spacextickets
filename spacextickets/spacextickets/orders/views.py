import json
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.forms import formset_factory
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from spacextickets.accounts.forms import TravelerForm
from spacextickets.accounts.models import BaseUser, Traveler
from spacextickets.core.models import ScheduledTrip
from spacextickets.utils.json import UUIDEncoder, UUIDDecoder
from spacextickets.utils.views import bad_boy, BadBoy
from spacextickets.utils.functions import to_date
from spacextickets.accounts.functions import add_guest, add_travelers
from .models import Ticket, Order
from .status import check_status, reset_status, set_status
from enum import Enum, unique


@unique
class OrderStatus(Enum):
    RESERVE = 0
    STEP1 = 1
    STEP2 = 2
    STEP3 = 3
    FINALIZE = 4
    ENUM_SIZE = 5


def confirm(request):
    try:
        seats = int(request.POST['seats'])
        trip1_id = request.POST['trip1_id']
        trip1_date = to_date(request.POST['trip1_date'])
        trip1 = ScheduledTrip.objects.get(id=trip1_id)
        trip2_id = request.POST.get('trip2_id', None)
        trip2_date = None
        trip2 = None

        reverse_kwargs = {'seats': seats,
                          'trip1_id': trip1_id,
                          'trip1_date': str(trip1_date)}

        if trip2_id:
            trip2_date = to_date(request.POST['trip2_date'])
            trip2 = ScheduledTrip.objects.get(id=trip2_id)
            reverse_kwargs['trip2_id'] = trip2_id
            reverse_kwargs['trip2_date'] = trip2_date

            if (trip2_date < trip1_date) or \
               (trip2_date == trip1_date and trip2.time < trip2.time) or \
               (trip1.departure != trip2.arrival or trip1.arrival != trip2.departure):
                raise BadBoy("Forged search request!")

        reserve_url = reverse("orders:reserve", kwargs=reverse_kwargs)
        context = {'seats': seats,
                   'trip1': trip1,
                   'trip2': trip2,
                   'trip1_date': trip1_date,
                   'trip2_date': trip2_date,
                   'reserve_url': reserve_url,
                   }

        return render(request, template_name="orders/confirm.html", context=context)
    except(ScheduledTrip.DoesNotExist, KeyError, ValidationError, BadBoy) as e:
        return bad_boy(request, e)


# Reserve an order (generating temporary tickets).
# An order (and its tickets) is reserved for 10 minutes. (cron clean-job)
def reserve(request, seats, trip1_id, trip1_date=None, trip2_id=None, trip2_date=None):
    try:
        seats = int(seats)
        if seats < 1:
            raise BadBoy("Trying to buy less than one seat.")

        # Delete any previous temporary order if present
        reset_status(request)

        # Retrieve trips and check for order's consistency
        trip1 = ScheduledTrip.objects.get(id=trip1_id)
        if trip2_date:
            trip2 = ScheduledTrip.objects.get(id=trip2_id)
            if (trip2_date < trip1_date) or \
               (trip2_date == trip1_date and trip2.time < trip2.time) or \
               (trip1.departure != trip2.arrival or trip1.arrival != trip2.departure):
                raise BadBoy("Forged reserve request!")

        # Check if the tickets are  still available
        if trip1.seats - Ticket.objects.filter(trip=trip1).count() < seats or\
           (trip2_date and (trip2.seats - Ticket.objects.filter(trip=trip2).count() < seats)):
            return render(request=request, template_name="orders/too_slow_error.html")

        # Create a new temporary order
        order = Order()
        if request.user.is_authenticated:
            order.user = request.user
        order.save()

        # Reserve the tickets
        for i in range(seats):
            Ticket.objects.create(order=order, trip=trip1, date=trip1_date)
            if trip2_date:
                Ticket.objects.create(order=order, trip=trip2, date=trip2_date)

        # Save the needed data to the session
        request.session['order'] = json.dumps(order.booking_code, cls=UUIDEncoder)
        request.session['seats'] = seats
        request.session.save()
        # Update the status (needed since check_status is not used here)
        set_status(OrderStatus.STEP1, request)

        # Redirect to "hide" the reservation link.
        return HttpResponseRedirect(reverse("orders:step1"))
    except(ScheduledTrip.DoesNotExist, BadBoy, ValidationError) as e:
        return bad_boy(request, e)


# Ask for guest users information.
@check_status(OrderStatus.STEP1)
def step1(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("orders:step2"))

    return render(request=request, template_name="orders/step1.html")


# Register guest user and fill the travelers information.
@check_status(OrderStatus.STEP2)
def step2(request):
    try:
        order = Order.objects.get(booking_code=json.loads(request.session['order'], cls=UUIDDecoder))
        if not request.user.is_authenticated:
            guest = add_guest(request)
            order.user = guest
        else:
            order.user = request.user  # Is this a base user or a normal one?
        order.save()

        formset = formset_factory(TravelerForm, extra=request.session['seats'])
        if request.user.is_authenticated:
            travelers = Traveler.objects.filter(user=request.user)
        else:
            travelers = None

        context = {'formset': formset, 'travelers': travelers}
        return render(request=request, template_name="orders/step2.html", context=context)
    except BadBoy as e:
        return bad_boy(request, e)


# Register the travelers && fake payment page
@check_status(OrderStatus.STEP3)
def step3(request):
    try:
        pl = dict()
        total = 0

        order = Order.objects.get(booking_code=json.loads(request.session['order'], cls=UUIDDecoder))
        user = order.user
        travelers = add_travelers(request, user)
        tickets = Ticket.objects.filter(order_id=json.loads(request.session['order'], cls=UUIDDecoder))

        i = 0
        for ticket in tickets.order_by('trip__id'):
            # Assign travelers to tickets
            ticket.traveler = travelers[i % len(travelers)]
            ticket.save()
            i += 1

            # Calculate prices, ticket numbers and total
            t = ticket.trip
            price = t.price + (pl[str(t)][0] if str(t) in pl else 0)
            count = 1 + (pl[str(t)][1] if str(t) in pl else 0)
            pl[str(t)] = (price, count)
            total += t.price

        context = {"prices_list": pl, 'total': total}

        return render(request=request, template_name="orders/step3.html", context=context)
    except(BadBoy, Traveler.DoesNotExist) as e:
        return bad_boy(request, e)


@check_status(OrderStatus.FINALIZE)
def finalize(request):
    try:
        order = Order.objects.get(booking_code=json.loads(request.session['order'], cls=UUIDDecoder))
        order.is_temporary = False
        order.save()
        del request.session['order']
        request.session.save()
        return HttpResponseRedirect(reverse("orders:detail", kwargs={'order_id': order.booking_code}))

    except(BadBoy, Ticket.DoesNotExist) as e:
        return bad_boy(request, e)


def detail(request, order_id):
    try:
        order = Order.objects.get(booking_code=order_id, is_temporary=False)

        if not order.user.is_guest():
            if not request.user.is_authenticated():
                login_url = reverse("accounts:login") + "?next=" + reverse("orders:detail", kwargs={'order_id': order_id})
                return HttpResponseRedirect(login_url)
            elif request.user.pk != order.user.pk:
                raise Http404()

        tickets = Ticket.objects.filter(order_id=order.booking_code)
        context = {'order': order, 'tickets': tickets}
        return render(request=request, template_name="orders/order_detail.html", context=context)
    except (Order.DoesNotExist, ValidationError):
        raise Http404()
