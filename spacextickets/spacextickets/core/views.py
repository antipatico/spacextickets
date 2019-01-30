from django.shortcuts import render
from .models import *


def index(req):
    return render(request=req, template_name="core/index.html")


def about(request):
    return render(request=request, template_name="core/about.html")