import sys
import os
import logging
from django.apps import AppConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
    is_started = False

    @staticmethod
    def init_db_clean(SportKind, SportSegment, Event, EventSegment, Factor):
        SportKind.objects.all().delete()
        SportSegment.objects.all().delete()
        Event.objects.all().delete()
        EventSegment.objects.all().delete()
        Factor.objects.all().delete()
        logger.info("DB cleanup complete")

    @staticmethod
    def init_sports(sports_data: list, SportKind, SportSegment):
        for sport in sports_data:
            if sport.get('kind') == 'sport':
                SportKind(fonkey=sport.get('id'), name=sport.get('name')).save()
            else:
                sport_kind = SportKind.objects.get(fonkey=sport.get('parentId'))
                SportSegment(fonkey=sport.get('id'), name=sport.get('name'), sport_kind=sport_kind).save()
        logger.info("SportKind/segment models initialization complete")

    @staticmethod
    def init_events(events_data: list, Event, EventSegment, SportSegment):
        for event in events_data:
            if event.get('name'):
                event_name = event.get('name')
            else:
                event_name = f"{event.get('team1', '')} - {event.get('team2', '')}"
            if event.get('level') == 1:
                event_ss = SportSegment.objects.get(fonkey=event.get('sportId'))
                event_sk = event_ss.sport_kind
                event_fullname = f"{event_sk.name} / {event_ss.name} / {event_name}"
                event_url = f"https://www.fonbet.ru/sports/{event_sk.fonkey}/{event_ss.fonkey}/{event.get('id')}"
                Event(fonkey=event.get('id'),
                      name=event_name,
                      full_name=event_fullname,
                      url=event_url,
                      is_live=event.get('place') == 'live',
                      start_time=event.get('startTime'),
                      sport_segment=event_ss
                      ).save()
            elif event.get('level') == 2:
                # print(event.get('level'), event.get('parentId'))
                parent_event = Event.objects.get(fonkey=event.get('parentId'))
                EventSegment(fonkey=event.get('id'),
                             name=event_name,
                             start_time=event.get('startTime'),
                             event=parent_event,
                             is_live=event.get('place') == 'live'
                             ).save()
            else:
                EventSegment(fonkey=event.get('id'),
                             name=event_name,
                             start_time=event.get('startTime'),
                             parent_id=event.get('parentId'),
                             is_live=event.get('place') == 'live'
                             ).save()
        logger.info("Events/EventSegments models initialization complete")

    @staticmethod
    def init_event_miscs(events_miscs: list, Event, EventSegment):
        for misc in events_miscs:
            current_event = Event.objects.get(fonkey=misc.get('id'))
            if not current_event:
                current_event = EventSegment.objects.get(fonkey=misc.get('id'))

        logger.info("SportKind/segment models initialization complete")

    def ready(self):
        if 'runserver' not in sys.argv:
            return True
        if os.environ.get('RUN_MAIN'):
            from .models import SportKind, SportSegment, Event, EventSegment, Factor
            from .fonbet_parser import EventsParser
            MainConfig.init_db_clean(SportKind, SportSegment, Event, EventSegment, Factor)
            initial_updates = EventsParser().get_updates()
            MainConfig.init_sports(initial_updates.get('sports'), SportKind, SportSegment)
            MainConfig.init_events(initial_updates.get('events'), Event, EventSegment, SportSegment)
            logger.info("All models initialization complete")
