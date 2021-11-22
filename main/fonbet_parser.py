import json
import requests
from django.conf import settings


class EventsParser:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = settings.FONBET_SESSION_HEADERS
        self.current_version = 0

    def get_updates(self):
        params = {'lang': 'ru',
                  'scopeMarket': 1600,
                  'version': self.current_version}
        url = 'https://line53.bkfon-resources.com/events/list'
        response = self.session.get(url, params=params)
        response.raise_for_status()
        updates_json = response.json()
        self.current_version = updates_json.get('packetVersion')
        return updates_json

    def get_server_timestamp(self):
        url = 'https://clientsapi12.bkfon-resources.com/serverTime'
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()['serverTime']

    @staticmethod
    def initial_dump(updates):
        sport_kinds = []
        sport_segments = []
        for sport in updates['sports']:
            if sport['kind'] == 'sport':
                sport_kinds.append(sport)
            elif sport['kind'] == 'segment':
                sport_segments.append(sport)
        EventsParser.dump(sport_kinds, 'json/sport_kinds.json')
        EventsParser.dump(sport_segments, 'json/sport_segments.json')
        EventsParser.dump(updates['events'], 'json/events.json')

    @staticmethod
    def dump(json_obj, path):
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(json_obj, file, indent=2, ensure_ascii=False)
