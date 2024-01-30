from datetime import datetime, timezone, timedelta
from math import ceil
from transportschedule.schedule.json_parse.json_parser import JsonParser


def convert_time(seconds: float):
    minutes = seconds // 60
    if minutes >= 60:
        return f'{int(minutes // 60)} час {int(minutes % 60)} мин.'
    return f'{int(minutes)} мин.'


class Processing:
    def __init__(self, json_data):
        self.json_data = json_data
        self.parser = JsonParser(self.json_data)

    def pagination(self):
        limit = self.parser.parse_json(self.json_data, 'limit')
        offset = self.parser.parse_json(self.json_data, 'offset')
        total = self.parser.parse_json(self.json_data, 'total')
        total_pages = ceil(total / limit)
        return limit, offset, total, total_pages

    def get_transport_route(self) -> tuple:
        from_station = self.parser.parse_json(self.json_data, 'from')
        to_station = self.parser.parse_json(self.json_data, 'to')
        station_type_name_from = from_station.get('station_type_name')
        title_from = self.parser.parse_json(from_station, 'title')
        station_type_name_to = to_station.get('station_type_name')
        title_to = self.parser.parse_json(to_station, 'title')
        return (
            station_type_name_from,
            title_from,
            station_type_name_to,
            title_to,
        )

    def detail_transport(self) -> list:
        segments = self.parser.parse_json(self.json_data, 'segments')
        route_info: list = list()
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
                route_info.append(
                    '\u00A0\u00A0#{1} | {0} ({3}) | {2}\u00A0\u00A0'.format(
                        departure_format_date,
                        number_route,
                        short_title_route,
                        duration,
                    )
                )
        return route_info
