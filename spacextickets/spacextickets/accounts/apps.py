from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AccountsConfig(AppConfig):
    name = 'spacextickets.accounts'
    verbose_name = _('SpaceX Tickets Accounts')
