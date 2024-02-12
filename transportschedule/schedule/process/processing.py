from datetime import datetime, timezone, timedelta
from typing import Any
from transportschedule.schedule.json_parse.json_parser import JsonParser
from transportschedule.schedule.request.request import RequestSchedule


def convert_time(seconds: str | float) -> str:
    minutes = int(seconds) // 60
    if minutes >= 60:
        return f'{int(minutes // 60)} час {int(minutes % 60)} мин.'
    return f'{int(minutes)} мин.'


class Processing:
    def __init__(self, json_data) -> None:
        self.json_data = json_data
        self.parser = JsonParser()

    def get_transport_route(self) -> tuple:
        from_station = self.parser.parse_json(self.json_data, 'from')
        from_code = self.parser.parse_json(from_station, 'code')
        to_station = self.parser.parse_json(self.json_data, 'to')
        to_code = self.parser.parse_json(to_station, 'code')
        title_from = self.parser.parse_json(from_station, 'title')
        title_to = self.parser.parse_json(to_station, 'title')
        return (
            from_code,
            title_from,
            to_code,
            title_to,
        )

    async def detail_transport(self) -> dict:
        segments = self.parser.parse_json(self.json_data, 'segments')
        route_stops: dict = {}

        utc_offset = timedelta(hours=3)
        current_time = timezone(utc_offset)
        current_datetime = datetime.now(current_time)
        count_results = 0
        for segment in segments:
            departure = self.parser.parse_json(segment, 'departure')
            date_departure = datetime.strptime(
                str(departure),
                '%Y-%m-%dT%H:%M:%S%z',
            )
            if date_departure > current_datetime:
                from_station = self.parser.parse_json(segment, 'from')
                to_station = self.parser.parse_json(segment, 'to')
                arrival = self.parser.parse_json(segment, 'arrival')
                date_arrival = datetime.strptime(
                    str(arrival),
                    '%Y-%m-%dT%H:%M:%S%z',
                )
                departure_format_date = date_departure.strftime('%H:%M')
                arrival_format_date = date_arrival.strftime('%H:%M')
                number_route = self.parser.parse_json(
                    segment,
                    'number',
                )
                thread_route = self.parser.parse_json(segment, 'thread')
                duration = convert_time(
                    self.parser.parse_json(segment, 'duration'),
                )
                short_title_route = self.parser.parse_json(
                    thread_route,
                    'short_title',
                )
                uid_thread = self.parser.parse_json(thread_route, 'uid')
                request = RequestSchedule(
                    uid=uid_thread,
                    from_station=from_station.get('code', None),
                    to_station=to_station.get('code', None),
                )
                threads = await request.request_thread_transport_route()
                days = self.parser.parse_json(threads.json(), 'days')
                stops = self.parser.parse_json(segment, 'stops')

                route_stops[uid_thread] = {
                    'route': '\u00A0\u00A0#{1} | {0} ({3}) | {2}\u00A0\u00A0'.format(
                        departure_format_date,
                        number_route,
                        short_title_route,
                        duration,
                    ),
                    'stops': stops,
                    'duration': duration,
                    'arrival': arrival_format_date,
                    'from': from_station,
                    'to': to_station,
                    'number': number_route,
                    'departure': departure_format_date,
                    'short_title_route': short_title_route,
                    'days': days,
                }
                count_results += 1
                if count_results >= 7:
                    break
        return route_stops

    def detail_thread(self) -> str:
        number = self.parser.parse_json(self.json_data, 'number')
        short_title = self.parser.parse_json(
            self.json_data,
            'short_title_route',
        )
        days = self.parser.parse_json(self.json_data, 'days')
        from_station = self.parser.parse_json(self.json_data, 'from')
        to_station = self.parser.parse_json(self.json_data, 'to')
        transport_type = self.parser.parse_json(
            from_station,
            'transport_type',
        )
        route_stops = self.parser.parse_json(self.json_data, 'stops')
        if not route_stops and transport_type == 'bus':
            route_stops = (
                'Автобусы и маршрутки обычно останавливаются на всех остановках'
            )
        duration = self.parser.parse_json(self.json_data, 'duration')
        arrival = self.parser.parse_json(self.json_data, 'arrival')
        to_title = self.parser.parse_json(to_station, 'title')
        stop_departure = self.parser.parse_json(self.json_data, 'departure')
        transport_type_name = 'Электричка'
        if transport_type == 'bus':
            transport_type_name = 'Автобус'
        return f'''<strong>{transport_type_name}:</strong> {number} {short_title}
<strong>График движения:</strong> {days}
<strong>Время отправления:</strong> {stop_departure}
<strong>С остановками:</strong> {route_stops}
<strong>Время в пути составит:</strong> {duration}
<strong>На конечный пункт {to_title} прибывает в:</strong> {arrival}
'''

    def station_list(self) -> dict[str, Any]:
        stations = self.parser.parse_json(self.json_data, 'stations')
        selected_stations = {}
        for station in stations:
            transport_type = self.parser.parse_json(
                station,
                'transport_type',
            )
            if transport_type == 'train':
                code = self.parser.parse_json(station, 'code')
                title = self.parser.parse_json(station, 'title')
                station_type_name = self.parser.parse_json(
                    station,
                    'station_type_name',
                )
                selected_stations[code] = {
                    'transport_type': transport_type,
                    'station_type_name': station_type_name,
                    'title': title,
                }
        return selected_stations

    def flight_schedule_station(self) -> dict[str, Any]:
        selected_flight_schedule_station: dict = {}
        utc_offset = timedelta(hours=3)
        current_time = timezone(utc_offset)
        current_datetime = datetime.now(current_time)
        schedule = self.parser.parse_json(self.json_data, 'schedule')
        count_results = 0
        for skd in schedule:
            departure = self.parser.parse_json(skd, 'departure')
            date_departure = datetime.strptime(
                str(departure),
                '%Y-%m-%dT%H:%M:%S%z',
            )
            if date_departure > current_datetime:
                uid = self.parser.parse_json(
                    skd,
                    'uid',
                )
                short_title = self.parser.parse_json(
                    skd,
                    'short_title',
                )
                stops = self.parser.parse_json(
                    skd,
                    'stops',
                )
                platform = self.parser.parse_json(
                    skd,
                    'platform',
                )
                number = self.parser.parse_json(
                    skd,
                    'number',
                )
                departure_format_time = date_departure.strftime('%H:%M')
                selected_flight_schedule_station[uid] = {
                    'short_title': short_title,
                    'stops': stops,
                    'platform': platform,
                    'number': number,
                    'departure_format_time': departure_format_time,
                }
                count_results += 1
                if count_results >= 10:
                    break
        return selected_flight_schedule_station
