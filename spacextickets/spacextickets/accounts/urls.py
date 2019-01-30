from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = "accounts"

urlpatterns = [
    url(r'^login/', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^register/', views.register_user, name="register"),
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^edit/$', views.edit_user, name='edit_user'),
    url(r'^password/$', views.password_change, name='change_password'),
    url(r'^travelers/$', views.show_travelers, name='travelers'),
    url(r'^travelers/edit/(?P<traveler_id>[0-9]+)/$', views.edit_traveler, name='edit_traveler'),
    url(r'^travelers/delete/(?P<traveler_id>[0-9]+)/$', views.del_traveler, name='del_traveler'),
]