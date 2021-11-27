from celery import shared_task
import os

from main.utils.fonbet_parser import EventsParser
from main.utils.model_updates import *

parser = EventsParser(current_version=os.environ.get('current_version'))


def update_sports(sports):
    for sport in sports:
        if sport.get('kind') == 'segment':
            if not SportSegment.objects.filter(fonkey=sport.get('id')):
                sport_kind = SportKind.objects.get(fonkey=sport.get('parentId'))
                SportSegment(fonkey=sport.get('id'), name=sport.get('name'), sport_kind=sport_kind).save()


def update_events(events):
    for event in events:
        if event.get('place') == 'notActive':
            if event.get('state') and event.get('state').get('willBeLive'):
                init_event(event)
            # else:
            #     if event.get('level') == 1:
            #         Event.objects.get(fonkey=event.get('id')).delete()
            #     else:
            #         EventSegment.objects.get(fonkey=event.get('id')).delete()
        elif event.get('place') == 'line':
            init_event(event)
        elif event.get('place') == 'live':
            if event.get('level') == 1:
                current_event = Event.objects.filter(fonkey=event.get('id')).first()
            else:
                current_event = EventSegment.objects.filter(fonkey=event.get('id')).first()

            if current_event:
                current_event.is_live = True
                current_event.save()
            else:
                init_event(event)


def update_miscs(miscs):
    for misc in miscs:
        init_event_misc(misc)


def update_factors(events):
    for event in events:
        is_event = True
        current_event = Event.objects.filter(fonkey=event.get('e')).first()
        if not current_event:
            is_event = False
            current_event = EventSegment.objects.filter(fonkey=event.get('e')).first()
        for factor in event.get('factors'):
            existing_factor = current_event.factors.filter(fonkey=factor.get('f')).first()
            if existing_factor:
                existing_factor.param = factor.get('p')
                existing_factor.value = factor.get('v')
                existing_factor.save()
            else:
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


@shared_task
def get_updates(name='get_updates'):
    updates_json = parser.get_updates()
    update_sports(updates_json.get('sports'))
    update_events(updates_json.get('events'))
    update_miscs(updates_json.get('eventMiscs'))
    update_factors(updates_json.get('customFactors'))
