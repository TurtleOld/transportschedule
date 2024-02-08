import json
import pathlib

from transportschedule.schedule.json_parse.json_parser import JsonParser


def test_json_parse():
    file = pathlib.Path(
        'transportschedule/schedule/tests/test_data/request.json',
    )

    with open(file) as json_data:
        data = json.load(json_data)

        parser = JsonParser()

        assert parser.parse_json(data, 'to') == {
            "code": "s9742891",
            "popular_title": "none",
            "short_title": "none",
            "station_type": "bus_stop",
            "station_type_name": "автобусная остановка",
            "title": "Северный посёлок",
            "transport_type": "bus",
            "type": "station",
        }
        assert parser.parse_json(data, 'to', 'title') == 'Северный посёлок'
