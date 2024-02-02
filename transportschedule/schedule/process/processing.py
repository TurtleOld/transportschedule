from datetime import datetime, timezone, timedelta

from transportschedule.schedule.json_parse.json_parser import JsonParser


def convert_time(seconds: float):
    minutes = seconds // 60
    if minutes >= 60:
        return f'{int(minutes // 60)} час {int(minutes % 60)} мин.'
    return f'{int(minutes)} мин.'


class Processing:
    def __init__(
        self,
        json_data,
        route_stops=None,
        route_duration=None,
        route_arrival=None,
    ):
        self.json_data = json_data
        self.parser = JsonParser(self.json_data)
        if route_stops is None:
            self.route_stops = {}
        self.route_stops = route_stops
        self.route_duration = route_duration
        self.route_arrival = route_arrival

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

    def detail_transport(self) -> tuple[list, list, dict, dict, dict]:
        segments = self.parser.parse_json(self.json_data, 'segments')
        route_info: list = list()
        route_detail_info: list = list()
        route_stops: dict = {}
        route_duration: dict = {}
        route_arrival: dict = {}
        utc_offset = timedelta(hours=3)
        current_time = timezone(utc_offset)
        current_datetime = datetime.now(current_time)

        for segment in segments:
            departure = self.parser.parse_json(segment, 'departure')
            date_departure = datetime.strptime(
                departure,
                '%Y-%m-%dT%H:%M:%S%z',
            )
            if date_departure > current_datetime:
                arrival = self.parser.parse_json(segment, 'arrival')
                date_arrival = datetime.strptime(
                    arrival,
                    '%Y-%m-%dT%H:%M:%S%z',
                )
                departure_format_date = date_departure.strftime('%H:%M')
                arrival_format_date = date_arrival.strftime('%H:%M')
                number_route = self.parser.parse_json(segment, 'number')
                thread_route = self.parser.parse_json(segment, 'thread')
                duration = convert_time(
                    self.parser.parse_json(segment, 'duration'),
                )
                short_title_route = self.parser.parse_json(
                    thread_route,
                    'short_title',
                )
                uid_thread = self.parser.parse_json(thread_route, 'uid')
                stops = self.parser.parse_json(segment, 'stops')
                route_info.append(
                    '\u00A0\u00A0#{1} | {0} ({3}) | {2}\u00A0\u00A0'.format(
                        departure_format_date,
                        number_route,
                        short_title_route,
                        duration,
                    )
                )
                route_detail_info.append(
                    uid_thread,
                )
                route_stops[uid_thread] = stops
                route_duration[uid_thread] = duration
                route_arrival[uid_thread] = arrival_format_date
        return (
            route_info,
            route_detail_info,
            route_stops,
            route_duration,
            route_arrival,
        )

    def detail_thread(self):
        number = self.parser.parse_json(self.json_data, 'number')
        short_title = self.parser.parse_json(self.json_data, 'short_title')
        days = self.parser.parse_json(self.json_data, 'days')
        from_station = self.parser.parse_json(self.json_data, 'from')
        to_station = self.parser.parse_json(self.json_data, 'to')
        transport_type = self.parser.parse_json(
            from_station,
            'transport_type',
        )
        uid_thread = self.parser.parse_json(self.json_data, 'uid')
        route_stops = self.route_stops.get(uid_thread, 'Нет информации!')
        if not route_stops and transport_type == 'bus':
            route_stops = (
                'Автобусы и маршрутки обычно останавливаются на всех остановках'
            )
        duration = self.route_duration.get(uid_thread, 'Нет информации!')
        arrival = self.route_arrival.get(uid_thread, 'Нет информации!')
        from_title = self.parser.parse_json(from_station, 'title')
        to_title = self.parser.parse_json(to_station, 'title')
        stops = self.parser.parse_json(self.json_data, 'stops')
        stop_departure = ''
        for stop in stops:
            stop_station = self.parser.parse_json(stop, 'station')
            stop_station_title = self.parser.parse_json(stop_station, 'title')
            if from_title == stop_station_title:
                stop_departure += stop['departure'][10:]
        transport_type_name = 'Электричка'
        if transport_type == 'bus':
            transport_type_name = 'Автобус'
        return f'''<strong>{transport_type_name}:</strong> {number} {short_title}
<strong>График движения:</strong> {days}
<strong>Время отправления:</strong> {stop_departure}
<strong>С остановками:</strong> {route_stops}
<strong>Время в пути составит:</strong> {duration}
<strong>В пункт прибытия {to_title} прибывает в:</strong> {arrival}
'''
