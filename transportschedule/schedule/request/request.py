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
        latitude: float = 0,
        longitude: float = 0,
        distance: int = 1,
        date: str = datetime.datetime.now().isoformat(),
        offset: int = 0,
        limit: int = 500,
        uid: str = '',
    ) -> None:
        self.transport_types: str = transport_types
        self.from_station: int = from_station
        self.to_station: int = to_station
        self.latitude: float = latitude
        self.longitude: float = longitude
        self.distance: int = distance
        self.date: str = date
        self.api_key: str | None = os.environ.get('YANDEX_API_KEY')
        self.search_url: str = 'https://api.rasp.yandex.net/v3.0/search/'
        self.thread_url: str = 'https://api.rasp.yandex.net/v3.0/thread/'
        self.nearest_stations: str = (
            'https://api.rasp.yandex.net/v3.0/nearest_stations/'
        )
        self.offset: int = offset
        self.limit: int = limit
        self.uid: str = uid

    def request_transport_between_stations(self) -> Response:
        params: dict[str, str | int | None] = {
            'apikey': self.api_key,
            'transport_types': self.transport_types,
            'from': f's{self.from_station}',
            'to': f's{self.to_station}',
            'date': self.date,
            'offset': self.offset,
            'limit': self.limit,
        }
        return requests.get(self.search_url, params=params)

    def request_thread_transport_route(self) -> Response:
        params: dict[str, str | int | None] = {
            'apikey': self.api_key,
            'uid': self.uid,
            'from': self.from_station,
            'to': self.to_station,
        }
        return requests.get(self.thread_url, params=params)

    def request_station_location(self) -> Response:
        params: dict[str, str | int | None] = {
            'apikey': self.api_key,
            'lat': self.latitude,
            'lng': self.longitude,
            'distance': self.distance,
        }
        return requests.get(self.nearest_stations, params=params)
