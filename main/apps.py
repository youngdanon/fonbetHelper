from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    @staticmethod
    def init_db_clean(SportKind, SportSegment, Event, EventSegment, Factor):
        SportKind.objects.all().delete()
        SportSegment.objects.all().delete()
        Event.objects.all().delete()
        EventSegment.objects.all().delete()
        Factor.objects.all().delete()

    @staticmethod
    def init_sports(sports_data: list, SportKind, SportSegment):
        for sport in sports_data:
            if sport.get('kind') == 'sport':
                SportKind(fonkey=sport.get('id'), name=sport.get('name')).save()
            else:
                sport_segment = SportSegment(fonkey=sport.get('id'), name=sport.get('name'))
                sport_segment.save()
                sport_kind = SportKind.objects.get(fonkey=sport.get('parentId'))
                sport_kind.segments = sport_segment

    def ready(self):
        print('ready')
        from .models import SportKind, SportSegment, Event, EventSegment, Factor
        from .fonbet_parser import EventsParser
        MainConfig.init_db_clean(SportKind, SportSegment, Event, EventSegment, Factor)
        initial_updates = EventsParser().get_updates()
        MainConfig.init_sports(initial_updates.get('sports'), SportKind, SportSegment)