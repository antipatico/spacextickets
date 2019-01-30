from django.conf.urls import url
from . import views

app_name = 'gmaps'

urlpatterns = [
    url(r'^$', views.show_maps, name='maps')
]