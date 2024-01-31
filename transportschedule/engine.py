import asyncio
import os

from aiohttp import web
from transportschedule.schedule.telegram.commands import start_bot, setup
from transportschedule.schedule.telegram.config import WEBHOOK_LISTEN, WEBHOOK_PORT


def main():
    """Engine."""
    if os.getenv('DEBUG'):
        asyncio.run(start_bot())
    else:
        web.run_app(
            setup(),
            host=WEBHOOK_LISTEN,
            port=WEBHOOK_PORT,
        )


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
