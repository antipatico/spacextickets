from django.shortcuts import render
from traceback import print_exception
import sys
import json
from django.utils.datetime_safe import datetime


class BadBoy(Exception):
    pass


def bad_boy(request, exception=None):
    print("[SECURITY-LOG] at \"%s %s\"" % (request.method, request.path))
    print("\tTimestamp:", datetime.now())
    print("\tIP:", request.META.get('REMOTE_ADDR'))
    forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded_for:
        print("\tHTTP_X_FORWARDED_FOR:", forwarded_for)
    user_agent = request.META.get('HTTP_USER_AGENT')
    if user_agent:
        print("\tUser-Agent:", user_agent)
    if request.user.is_authenticated:
        print("\tUser: %s (id %s)" % (request.user.get_full_name(), request.user.id))
    if request.method == "POST":
        print("\tPOST data:", json.dumps(request.POST))
    if exception:
        print_exception(type(exception), exception, sys.exc_info()[2], file=sys.stdout)

    return render(request, template_name="utils/bad_boy.html")
