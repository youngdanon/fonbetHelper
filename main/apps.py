from django.apps import AppConfig



class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    @staticmethod
    def initial_db_clean(SportKind, SportSegment, Event, EventSegment, Factor):
        SportKind.objects.all().delete()
        SportSegment.objects.all().delete()
        Event.objects.all().delete()
        EventSegment.objects.all().delete()
        Factor.objects.all().delete()

    def ready(self):
        from .models import SportKind, SportSegment, Event, EventSegment, Factor
        MainConfig.initial_db_clean(SportKind, SportSegment, Event, EventSegment, Factor)

