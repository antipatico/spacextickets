#!/usr/bin/env bash

if [ "${DEBUG}" ]; then
    set -x
fi

source "$(dirname $0)/functions.sh"

set -e

path=$(get_path)

pushd "${path}" > /dev/null
cat << EOF | ./manage.py shell
from sys import exit
from datetime import time
from datetime import timedelta as duration
from spacextickets.core.models import *
from spacextickets.gmaps.models import *

def sched_rt(city1, city2, wd, t, d=duration(minutes=13, seconds=37), p=1337.69, s=5):
    from spacextickets.core.models import ScheduledTrip
    ScheduledTrip.objects.get_or_create(departure=city1, arrival=city2, week_day=wd, time=t, duration=d, price=p, seats=s)
    ScheduledTrip.objects.get_or_create(departure=city2, arrival=city1, week_day=wd, time=t, duration=d, price=p, seats=s)


# Populate States
italy, _ = State.objects.get_or_create(name_en="Italy", name_it="Italia", continent="EU")
france, _ = State.objects.get_or_create(name_en="France", name_it="Francia", continent="EU")
netherlands, _ = State.objects.get_or_create(name_en="Netherlands", name_it="Paesi Bassi", continent="EU")
newyork, _ = State.objects.get_or_create(name_en="New York", name_it="New York", continent="NA")
california, _ = State.objects.get_or_create(name_en="California", name_it="California", continent="NA")
canada, _ = State.objects.get_or_create(name_en="Canada", name_it="Canada", continent="NA")
china, _ = State.objects.get_or_create(name_en="China", name_it="Cina", continent="AS")

# Populate Cities
modena, _ = City.objects.get_or_create(name_en="Modena", name_it="Modena", state=italy)
rome, _ = City.objects.get_or_create(name_en="Rome", name_it="Roma", state=italy)
milan, _ = City.objects.get_or_create(name_en="Milan", name_it="Milano", state=italy)
turin, _ = City.objects.get_or_create(name_en="Turin", name_it="Torino", state=italy)
palermo, _ = City.objects.get_or_create(name_en="Palermo", name_it="Palermo", state=italy)
paris, _ = City.objects.get_or_create(name_en="Paris", name_it="Parigi", state=france)
nice, _ = City.objects.get_or_create(name_en="Nice", name_it="Nizza", state=france)
marseille, _ = City.objects.get_or_create(name_en="Marseille", name_it="Marsiglia", state=france)
amsterdam, _ = City.objects.get_or_create(name_en="Amsterdam", name_it="Amsterdam", state=netherlands)
groningen, _ = City.objects.get_or_create(name_en="Groningen", name_it="Groninga", state=netherlands)
rotterdam, _ = City.objects.get_or_create(name_en="Rotterdam", name_it="Rotterdam", state=netherlands)
vancouver, _ = City.objects.get_or_create(name_en="Vancouver", name_it="Vancouver", state=canada)
los_angeles, _ = City.objects.get_or_create(name_en="Los Angeles", name_it="Los Angeles", state=california)
newyork_city, _ = City.objects.get_or_create(name_en="New York", name_it="New York", state=newyork)


# Populate ScheduledTrips
for wd in range(0,7):
    for t in [time(hour=0, minute=0), time(hour=13,minute=37), time(hour=16,minute=20), time(hour=23,minute=59)]:
        sched_rt(modena, palermo, wd, t)
        sched_rt(modena, rome, wd, t)
        sched_rt(modena, vancouver, wd, t)
        sched_rt(modena, los_angeles, wd, t)
        sched_rt(rome, milan, wd, t)
        sched_rt(turin, rome, wd, t)
        sched_rt(rome, newyork_city, wd, t)
        sched_rt(newyork_city, vancouver, wd, t)
        sched_rt(amsterdam, los_angeles, wd, t)
        sched_rt(groningen, newyork_city, wd, t)
        sched_rt(paris, palermo, wd, t)
        sched_rt(paris, vancouver, wd, t)
        sched_rt(los_angeles, rotterdam, wd, t)
        sched_rt(nice, marseille, wd, t)
        sched_rt(marseille, turin, wd, t)
        sched_rt(groningen, palermo, wd, t)
        sched_rt(palermo, milan, wd, t)

# Populate CityMap (thanks latlong.net)
Marker.objects.get_or_create(city=modena, lat=44.633793, long=10.944750)
Marker.objects.get_or_create(city=rome, lat=41.902783, long=12.496366)
Marker.objects.get_or_create(city=milan, lat=45.464204, long=9.189982)
Marker.objects.get_or_create(city=turin, lat=45.070339, long=7.686864)
Marker.objects.get_or_create(city=palermo, lat=38.115688, long=13.361267)
Marker.objects.get_or_create(city=paris, lat=48.856614, long=2.352222)
Marker.objects.get_or_create(city=nice, lat=43.710173, long=7.261953)
Marker.objects.get_or_create(city=marseille, lat=43.296482, long=5.369780)
Marker.objects.get_or_create(city=amsterdam, lat=52.370216, long=4.895168)
Marker.objects.get_or_create(city=groningen, lat=53.219383, long=6.566502)
Marker.objects.get_or_create(city=rotterdam, lat=51.924420, long=4.477733)
Marker.objects.get_or_create(city=vancouver, lat=49.282729, long=-123.120738)
Marker.objects.get_or_create(city=los_angeles, lat=34.052234, long=-118.243685)
Marker.objects.get_or_create(city=newyork_city, lat=40.712775, long=-74.005973)
EOF
popd > /dev/null
exit 0