from django.apps import AppConfig


class CoreAppConfig(AppConfig):
    name = 'brabbl.core'

    def ready(self):
        from . import signals  # NOQA
