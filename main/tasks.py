from celery import shared_task
import os

from main.utils.fonbet_parser import EventsParser

parser = EventsParser(current_version=os.environ.get('current_version'))


# def update_events(events):
#     for event in events:
#         if event.get('announced') or event.get('place') == 'line':


@shared_task
def get_updates():
    updates_json = parser.get_updates()
