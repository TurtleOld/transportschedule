import asyncio
import datetime
import json

from icecream import ic

from transportschedule.schedule.process.processing import Processing
from transportschedule.schedule.request.request import RequestSchedule
from transportschedule.schedule.telegram.commands import start_bot


def main():
    """Engine."""

    asyncio.run(start_bot())


if __name__ == '__main__':
    main()


# def main():
# request = RequestSchedule(
#     'bus',
#     9742908,
#     9742891,
#     datetime.datetime.today(),
#     offset=100,
# )
# result = request.request_transport_between_stations()
# ic(result)
# with open(
#     'schedule/tests/test_data/request.json',
#     'r',
# ) as json_data:
#     data = json_data.read()
#     parsed_json = json.loads(data)
#     process = Processing(parsed_json)
#     result_pagination = process.pagination()
#     result_route = process.get_transport_route()
#     ic(result_pagination)
#     ic(result_route)
