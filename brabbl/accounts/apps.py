from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AccountsConfig(AppConfig):
    name = 'brabbl.accounts'
    verbose_name = _('User')

    def ready(self):
        from . import signals  # NOQA
