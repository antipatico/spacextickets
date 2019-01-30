from django.conf.urls import url
from . import views

app_name = 'orders'

urlpatterns = [
    url(r'^reserve/(?P<seats>\d+)/(?P<trip1_id>[\dA-Za-z\-]{36})/(?P<trip1_date>\d{4}-\d{2}-\d{2})/$',
        views.reserve, name='reserve'),
    url(r'^reserve/(?P<seats>\d+)/(?P<trip1_id>[\dA-Za-z\-]{36})/(?P<trip1_date>\d{4}-\d{2}-\d{2})/'
        r'(?P<trip2_id>[\dA-Za-z\-]{36})/(?P<trip2_date>\d{4}-\d{2}-\d{2})/$', views.reserve, name='reserve'),
    url(r'^confirm/$', views.confirm, name='confirm'),
    url(r'^step1/$', views.step1, name='step1'),
    url(r'^step2/$', views.step2, name='step2'),
    url(r'^step3/$', views.step3, name='step3'),
    url(r'^finalize/$', views.finalize, name='finalize'),
    url(r'^detail/(?P<order_id>[\dA-Za-z\-]{36})/$', views.detail, name='detail'),
]
