import datetime
import os
from typing import Dict, Any

import dotenv
import requests
from icecream import ic
from requests import Response

dotenv.load_dotenv()


class RequestSchedule:

    def __init__(
        self,
        transport_types: str = '',
        from_station: int = 0,
        to_station: int = 0,
        date: str = datetime.datetime.now().isoformat(),
        offset: int = 0,
        limit: int = 500,
        uid: str = '',
    ) -> None:
        self.transport_types: str = transport_types
        self.from_station: int = from_station
        self.to_station: int = to_station
        self.date: str = date
        self.api_key: str | None = os.environ.get('YANDEX_API_KEY')
        self.search_url: str = 'https://api.rasp.yandex.net/v3.0/search/'
        self.thread_url: str = 'https://api.rasp.yandex.net/v3.0/thread/'
        self.offset: int = offset
        self.limit: int = limit
        self.uid: str = uid

    def request_transport_between_stations(self) -> Dict[str, str | int]:
        params: dict[str, str | int | None] = {
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

    def request_thread_transport_route(self) -> Dict[str, str | int]:
        params: dict[str, str | int | None] = {
            'apikey': self.api_key,
            'uid': self.uid,
            'from': self.from_station,
            'to': self.to_station,
        }
        request: Response = requests.get(self.thread_url, params=params)
        return request.json()
