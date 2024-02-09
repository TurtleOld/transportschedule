import datetime
import os
import dotenv
import requests
from requests import Response

from transportschedule.schedule.request.httprequest import request_schedule

dotenv.load_dotenv()


class RequestSchedule:

    def __init__(
        self,
        transport_types: str = '',
        from_station: int = 0,
        to_station: int = 0,
        current_station: str = '',
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
        self.current_station: str = current_station
        self.latitude: float = latitude
        self.longitude: float = longitude
        self.distance: int = distance
        self.date: str = date
        self.api_key: str | None = os.environ.get('YANDEX_API_KEY')
        self.search_url: str = 'search/'
        self.thread_url: str = 'thread/'
        self.nearest_stations_url: str = 'nearest_stations/'
        self.schedule_url: str = 'schedule/'
        self.offset: int = offset
        self.limit: int = limit
        self.uid: str = uid

    async def request_transport_between_stations(self) -> Response:
        params: dict[str, str | int | None] = {
            'apikey': self.api_key,
            'transport_types': self.transport_types,
            'from': f's{self.from_station}',
            'to': f's{self.to_station}',
            'date': self.date,
            'offset': self.offset,
            'limit': self.limit,
        }
        return await request_schedule(self.search_url, params=params)

    async def request_thread_transport_route(self) -> Response:
        params: dict[str, str | int | None] = {
            'apikey': self.api_key,
            'uid': self.uid,
            'from': self.from_station,
            'to': self.to_station,
            'limit': self.limit,
        }
        return await request_schedule(self.thread_url, params=params)

    async def request_station_location(self) -> Response:
        params: dict[str, str | int | None] = {
            'apikey': self.api_key,
            'lat': self.latitude,
            'lng': self.longitude,
            'distance': self.distance,
            'limit': self.limit,
        }
        return await request_schedule(self.nearest_stations_url, params=params)

    async def request_flight_schedule_station(self) -> Response:
        params: dict[str, str | int | None] = {
            'apikey': self.api_key,
            'date': self.date,
            'station': self.current_station,
            'limit': self.limit,
        }
        return await request_schedule(self.schedule_url, params=params)
