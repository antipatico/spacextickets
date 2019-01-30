"""spacextickets URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language
from spacextickets.utils.views import bad_boy

BAD_BOYS = ['phpMyAdmin', 'backups', 'admin', 'webmail', '.bash_history', '.bashrc', '.htaccess', 'passwords',
            'secrets', 'l33t', 'ftp', 'downloads', 'private']

urlpatterns = [
    url(r'^setlang/', set_language, name='set_language'),
] + i18n_patterns(
    url(r'^django-admin/', admin.site.urls, name="admin"),
    url(r'^', include('spacextickets.core.urls')),
    url(r'^search/', include('spacextickets.search.urls')),
    url(r'^orders/', include('spacextickets.orders.urls')),
    url(r'^accounts/', include('spacextickets.accounts.urls')),
    url(r'^maps/', include('spacextickets.gmaps.urls')),
)

for bb in BAD_BOYS:
    urlpatterns += [url(r'^%s/' % bb, bad_boy)] + i18n_patterns(url(r'^%s/' % bb, bad_boy))
