from datetime import datetime, timezone, timedelta
from math import ceil

from icecream import ic

from transportschedule.schedule.json_parse.json_parser import JsonParser
from transportschedule.schedule.request.request import RequestSchedule


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

    def detail_transport(self) -> tuple[list, list]:
        segments = self.parser.parse_json(self.json_data, 'segments')
        route_info: list = list()
        route_detail_info: list = list()
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
        return route_info, route_detail_info

    def detail_thread(self):
        ic(self.json_data)
        number = self.parser.parse_json(self.json_data, 'number')
        short_title = self.parser.parse_json(self.json_data, 'short_title')
        days = self.parser.parse_json(self.json_data, 'days')
        from_station = self.parser.parse_json(self.json_data, 'from')
        to_station = self.parser.parse_json(self.json_data, 'to')
        return (
            '<strong>Электричка:</strong> {} {}\n <strong>График хождения:</strong> {}'
        ).format(number, short_title, days)
