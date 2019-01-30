from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from spacextickets.core.models import ScheduledTrip
from spacextickets.search.functions import search_trips
from spacextickets.utils.views import bad_boy
from spacextickets.utils.functions import to_date, to_time
from .forms import *


def search_return(request):
    if request.method == 'GET':
        return HttpResponseRedirect(reverse("core:index"))
    elif request.method == 'POST':
        try:
            current_lang = request.LANGUAGE_CODE

            seats = int(request.POST['seats'])
            trip1_date = to_date(request.POST['trip1_date'])
            trip1_id = request.POST['trip1_id']
            trip2_date = to_date(request.POST['trip2_date'])
            trip2_time = to_time(request.POST['trip2_time'], loose=True)

            trip1 = ScheduledTrip.objects.get(id=trip1_id)
            departure = trip1.arrival
            arrival = trip1.departure
            search_results = search_trips(departure, arrival, trip2_date, trip2_time, seats, current_lang)

            context = {'available_trips': search_results,
                       'roundtrip': False,
                       'seats': seats,
                       'trip1_id': trip1_id,
                       'trip1_date': str(trip1_date),
                       'trip2_date': str(trip2_date)}

            return render(request=request, template_name="search/results.html", context=context)
        except (ScheduledTrip.DoesNotExist, ValidationError, ValueError) as e:
            return bad_boy(request, exception=e)


def search(request):
    context = {}
    if request.method == 'GET':
        return HttpResponseRedirect(reverse("core:index"))
    elif request.method == 'POST':
        form = SearchForm(request.POST)
        #context['form'] = form

        if form.is_valid():
            departure = form.cleaned_data['departure']
            arrival = form.cleaned_data['arrival']
            dep_date = form.cleaned_data['dep_date']
            ret_date = form.cleaned_data['ret_date']
            seats = form.cleaned_data['seats']
            dep_time = form.cleaned_data['dep_time']
            ret_time = form.cleaned_data['ret_time']
            current_lang = request.LANGUAGE_CODE

            search_results = search_trips(departure, arrival, dep_date, dep_time, seats, current_lang)
            roundtrip = (ret_date is not None)

            context['available_trips'] = search_results
            context['roundtrip'] = roundtrip
            context['seats'] = seats
            context['trip1_date'] = str(dep_date)
            context['trip2_date'] = str(ret_date)
            context['trip2_time'] = ret_time

    return render(request=request, template_name="search/results.html", context=context)