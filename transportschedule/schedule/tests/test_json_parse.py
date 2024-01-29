import pathlib

from icecream import ic


def test_json_parse():
    file = pathlib.Path(
        'transportschedule/schedule/tests/test_data/request.json',
    )
    with open(file) as json_data:
        data = json_data.read()
        ic(data)
