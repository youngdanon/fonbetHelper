import json
import requests
from django.conf import settings


class EventsParser:
    def __init__(self, current_version=0):
        self.session = requests.Session()
        self.session.headers = settings.FONBET_SESSION_HEADERS
        self.current_version = current_version

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
