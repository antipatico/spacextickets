from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class CoreConfig(AppConfig):
    name = 'spacextickets.core'
    verbose_name = _('SpaceX Tickets Core')
