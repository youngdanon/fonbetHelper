import sys
import os
import logging
from django.apps import AppConfig
from .server_startup import on_startup


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
    is_started = False

    def ready(self):
        if 'runserver' not in sys.argv:
            return True
        if os.environ.get('RUN_MAIN'):
            on_startup()
