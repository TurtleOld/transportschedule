import datetime
import os

import requests
from dotenv import load_dotenv

from transportschedule import constants
from transportschedule.schedule.request.request import RequestSchedule

load_dotenv()


def test_request_transport_between_stations():
    request = RequestSchedule(
        transport_types='bus',
        from_station=constants.BUS_STATION_SERGIEV_POSAD,
        to_station=constants.BUS_STOP_NORTH_VILLAGE,
        date=datetime.datetime.now().isoformat(),
    )
    response = request.request_transport_between_stations()

    assert response.status_code == 200


def test_api_error():

    params = {
        'apikey': os.getenv('YANDEX_API_KEY'),
        'transport_types': 'bus',
        'from': 97429,
        'to': 97428,
        'date': datetime.datetime.now().isoformat(),
        'limit': 500,
    }

    url_search = 'https://api.rasp.yandex.net/v3.0/search/'

    response = requests.get(url_search, params=params)

    assert response.status_code == 404

    assert (
        response.json().get('error').get('text')
        == 'Не нашли объект по yandex коду 97429'
    )
