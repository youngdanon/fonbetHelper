import sys
import os
from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
    is_started = False

    def ready(self):
        if 'runserver' not in sys.argv:
            return True
        if os.environ.get('RUN_MAIN'):
            from main.utils.server_startup import on_startup
            on_startup()
