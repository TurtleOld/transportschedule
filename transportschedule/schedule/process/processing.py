from datetime import datetime, timezone, timedelta

from transportschedule.schedule.json_parse.json_parser import JsonParser


def convert_time(seconds: float):
    minutes = seconds // 60
    if minutes >= 60:
        return f'{int(minutes // 60)} час {int(minutes % 60)} мин.'
    return f'{int(minutes)} мин.'


class Processing:
    def __init__(self, json_data, route_stops=None):
        self.json_data = json_data
        self.parser = JsonParser(self.json_data)
        if route_stops is None:
            self.route_stops = {}
        self.route_stops = route_stops

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

    def detail_transport(self) -> tuple[list, list, dict]:
        segments = self.parser.parse_json(self.json_data, 'segments')
        route_info: list = list()
        route_detail_info: list = list()
        route_stops: dict = {}
        utc_offset = timedelta(hours=3)
        current_time = timezone(utc_offset)
        current_datetime = datetime.now(current_time)
        for segment in segments:
            departure = self.parser.parse_json(segment, 'departure')

            date = datetime.strptime(
                departure,
                '%Y-%m-%dT%H:%M:%S%z',
            )
            if date > current_datetime:
                departure_format_date = date.strftime('%H:%M')
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
        return route_info, route_detail_info, route_stops

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

        from_title = self.parser.parse_json(from_station, 'title')
        to_title = self.parser.parse_json(to_station, 'title')
        stops = self.parser.parse_json(self.json_data, 'stops')
        stop_departure = ''
        arrival = ''
        duration = float()
        for stop in stops:
            stop_station = self.parser.parse_json(stop, 'station')
            stop_station_title = self.parser.parse_json(stop_station, 'title')
            if from_title == stop_station_title:
                stop_departure += stop['departure'][10:]
            if to_title == stop_station_title:
                arrival += stop['arrival'][10:]
                duration += stop['duration']
        transport_type_name = 'Электричка'
        if transport_type == 'bus':
            transport_type_name = 'Автобус'
        return f'''<strong>{transport_type_name}:</strong> {number} {short_title}
<strong>График хождения:</strong> {days}
<strong>Время отправления:</strong> {stop_departure}
<strong>С остановками:</strong> {route_stops}
<strong>Время в пути:</strong> {convert_time(duration)}
<strong>Приезжает на конечную станцию:</strong> {to_title} в {arrival}
'''
