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
            current_event = Event.objects.filter(fonkey=misc.get('id')).first()
            if not current_event:
                current_event = EventSegment.objects.filter(fonkey=misc.get('id')).first()
            current_event.score_comment = misc.get('comment')
            current_event.score1 = misc.get('score1')
            current_event.score2 = misc.get('score2')
            current_event.save()
        logger.info("Miscs initialization complete")

    @staticmethod
    def init_factors(factors: list, Event, EventSegment, Factor):
        for event in factors:
            is_event = True
            current_event = Event.objects.filter(fonkey=event.get('e')).first()
            if not current_event:
                is_event = False
                current_event = EventSegment.objects.filter(fonkey=event.get('e')).first()
            for factor in event.get('factors'):
                if is_event:
                    Factor(fonkey=factor.get('f'),
                           param=factor.get('p'),
                           value=factor.get('v'),
                           event=current_event).save()
                else:
                    Factor(fonkey=factor.get('f'),
                           param=factor.get('p'),
                           value=factor.get('v'),
                           event_segment=current_event).save()
        logger.info("Factors initialization complete")

    @staticmethod
    def init_event_blocks(event_blocks: list, Event, EventSegment, Factor):
        for block in event_blocks:
            current_event = Event.objects.filter(fonkey=block.get('eventId')).first()
            if not current_event:
                current_event = EventSegment.objects.filter(fonkey=block.get('eventId')).first()
            if block.get('state') == 'blocked':
                current_event.is_blocked = True
            elif block.get('state') == 'unblocked':
                current_event.is_blocked = False
            elif block.get('state') == 'partial':
                for factor_fonkey in block.get('factors'):
                    # print(factor_fonkey)
                    # print(current_event.factors.all())
                    factor = current_event.factors.filter(fonkey=factor_fonkey).first()
                    print(factor)
                    if not factor:
                        continue
                    factor.is_blocked = True
                    factor.save()
            current_event.save()
        logger.info("Event blocks initialization complete")

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
            MainConfig.init_event_miscs(initial_updates.get('eventMiscs'), Event, EventSegment)
            MainConfig.init_factors(initial_updates.get('customFactors'), Event, EventSegment, Factor)
            MainConfig.init_event_blocks(initial_updates.get('eventBlocks'), Event, EventSegment, Factor)
            logger.info("All models initialization complete")
