from math import ceil

from icecream import ic

from transportschedule.schedule.json_parse.json_parser import JsonParser


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
