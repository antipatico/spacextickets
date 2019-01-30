import json
from django.shortcuts import render

from spacextickets.orders.functions import delete_session_order
from spacextickets.utils.json import OrderStatusDecoder, OrderStatusEncoder
from spacextickets.utils.views import bad_boy, BadBoy


def set_status(status, request):
    request.session['status'] = json.dumps(status, cls=OrderStatusEncoder)
    request.session.save()


def reset_status(request):
    from spacextickets.orders.views import OrderStatus
    delete_session_order(request)
    set_status(OrderStatus(0), request)


def check_status(status, error_template="orders/back_and_forth_error.html", expired_template="orders/expired_error.html"):
    def real_decorator(f):
        def decorator(request, *args, **kwargs):
            from spacextickets.orders.views import OrderStatus
            from spacextickets.orders.models import Order

            if status != OrderStatus(0) and ("status" not in request.session or not request.session['status']):
                reset_status(request)
                return bad_boy(request, BadBoy("NULL session['status']!"))
            try:
                current_status = json.loads(request.session['status'], cls=OrderStatusDecoder)
            except:
                current_status = OrderStatus(0)
            if current_status.value < status.value:
                reset_status(request)
                return bad_boy(request, BadBoy("session['status'] < status"))
            elif current_status.value > status.value:
                reset_status(request)
                return render(request, template_name=error_template)

            set_status(OrderStatus((current_status.value + 1) % OrderStatus.ENUM_SIZE.value), request)
            try:
                return f(request, *args, **kwargs)
            except Order.DoesNotExist:
                return render(request, template_name=expired_template)

        return decorator

    return real_decorator
