import datetime
import os

import dotenv
import requests
from requests import Response

dotenv.load_dotenv()


class RequestSchedule:

    def __init__(
        self,
        transport_types='',
        from_station=0,
        to_station=0,
        date=datetime.datetime.now().isoformat(),
        offset=0,
        limit=500,
        uid='',
    ) -> None:
        self.transport_types: str = transport_types
        self.from_station: int = from_station
        self.to_station: int = to_station
        self.date: str = date
        self.api_key: str = os.environ.get('YANDEX_API_KEY')
        self.search_url: str = 'https://api.rasp.yandex.net/v3.0/search/'
        self.thread_url: str = 'https://api.rasp.yandex.net/v3.0/thread/'
        self.offset = offset
        self.limit = limit
        self.uid = uid

    def request_transport_between_stations(self) -> dict:
        params: dict = {
            'apikey': self.api_key,
            'transport_types': self.transport_types,
            'from': f's{self.from_station}',
            'to': f's{self.to_station}',
            'date': self.date,
            'offset': self.offset,
            'limit': self.limit,
        }
        request: Response = requests.get(self.search_url, params=params)
        return request.json()

    def request_thread_transport_route(self) -> dict:
        params: dict = {
            'apikey': self.api_key,
            'uid': self.uid,
            'from': self.from_station,
            'to': self.to_station,
        }
        request: Response = requests.get(self.thread_url, params=params)
        return request.json()
