#!/usr/bin/env bash

if [ "${DEBUG}" ]; then
    set -x
fi

PROJECT_PATH="spacextickets"

WEEKS=0
DAYS=0
HOURS=0
MINUTES=0
SECONDS=5

set -e


pushd "${PROJECT_PATH}" > /dev/null
cat << EOF | ./manage.py shell
from django.utils.timezone import datetime
from datetime import timedelta
from spacextickets.orders.functions import delete_order
from spacextickets.orders.models import Order

now = datetime.now()
ten_minutes_ago = now - timedelta(weeks=$WEEKS, days=$DAYS, hours=$HOURS, minutes=$MINUTES, seconds=$SECONDS)
expired_orders = Order.objects.filter(is_temporary=True, order_date__lte=ten_minutes_ago)
count = expired_orders.count()
for order in expired_orders:
    delete_order(order.pk)
if count > 0:
    print("Deleted %d temporary orders" % count)
EOF
popd > /dev/null
exit 0