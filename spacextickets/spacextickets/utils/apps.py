from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class UtilsConfig(AppConfig):
    name = 'spacextickets.utils'
    verbose_name = _("SpaceX Tickets Utils");