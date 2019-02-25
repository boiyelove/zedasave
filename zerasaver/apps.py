from django.apps import AppConfig


class ZerasaverConfig(AppConfig):
    name = 'zerasaver'

    def ready(self):
    	from . import signals