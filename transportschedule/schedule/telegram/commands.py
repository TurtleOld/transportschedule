import json
import os
import re
from typing import Any, Dict

from icecream import ic
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from telebot import types

from transportschedule.schedule.database.connect import DATABASE_URL
from transportschedule.schedule.database.tables import UserRoute
from transportschedule.schedule.encode import encode_string, check_login
from transportschedule.schedule.process.processing import Processing
from transportschedule.schedule.request.request import RequestSchedule
from transportschedule.schedule.telegram.config import bot
from transportschedule.schedule.telegram.keyboard import (
    select_transport_type,
    selected_bus,
    selected_route,
    selected_suburban,
    back_main,
    send_message,
    keyboard_station,
    back_from_routes,
)


async def create_database_session():
    """Create database session."""
    engine = create_async_engine(DATABASE_URL)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        return session


@bot.message_handler(content_types=['location'])
async def handle_location(message: types.Message):
    location = RequestSchedule(
        longitude=message.location.longitude,
        latitude=message.location.latitude,
    )
    result_response_location = await location.request_station_location()
    response = result_response_location.json()
    process_station = Processing(response)
    result_station = process_station.station_list()
    await keyboard_station(message, result_station)


@bot.message_handler(commands=['select'])  # type: ignore
async def handler_command_request(message: types.Message) -> None:
    salt, login = encode_string(message.from_user.username)
    result_check = check_login(salt, message.from_user.username)
    ic(login[16:] == result_check)
    await select_transport_type(message)


@bot.callback_query_handler(
    func=lambda call: re.match(r's\d+', call.data),
)  # type: ignore
async def handle_stations(call: types.CallbackQuery) -> None:
    try:
        transport_route = ''
        station_response = RequestSchedule(current_station=call.data)
        result_station_response = (
            await station_response.request_flight_schedule_station()
        )
        process_station_response = Processing(result_station_response.json())
        result = process_station_response.flight_schedule_station()
        for key, value in result.items():
            departure_format_time = value.get('departure_format_time')
            number = value.get('number')
            short_title = value.get('short_title')
            stops = value.get('stops')
            transport_route += f'''
            
{departure_format_time}
{number} {short_title}
С остановками {stops}'''

        await back_from_routes(call.message, transport_route)
    except Exception as error:
        await bot.send_message(call.message.chat.id, error)


@bot.callback_query_handler(
    func=lambda call: call.data == 'bus',
)  # type: ignore
async def callback_handler_bus(call: types.CallbackQuery) -> None:
    try:
        await bot.delete_message(call.message.chat.id, call.message.id)
        sent_message = await bot.send_message(
            call.message.chat.id,
            'Выбран вид транспорта: Автобус',
        )
        send_message.append(sent_message)
        await selected_bus(call.message)
    except Exception as error:
        await bot.send_message(call.message.chat.id, error)


@bot.callback_query_handler(
    func=lambda call: call.data == 'suburban',
)  # type: ignore
async def callback_handler_suburban(call: types.CallbackQuery) -> None:
    try:
        await bot.delete_message(call.message.chat.id, call.message.id)
        sent_message = await bot.send_message(
            call.message.chat.id,
            'Выбран вид транспорта: Электричка',
        )
        send_message.append(sent_message)
        await selected_suburban(call.message)
    except Exception as error:
        await bot.send_message(call.message.chat.id, error)


async def handler_request_transport(
    call: types.CallbackQuery,
) -> Dict[str, str | int] | None:
    try:
        current_directory = os.path.dirname(__file__)
        file_name = 'routes.json'
        file_path = os.path.abspath(os.path.join(current_directory, file_name))
        with open(file_path, 'r') as route_file:
            json_route = json.load(route_file)

        for key, value in json_route.items():
            if key == call.data:
                sent_message = await bot.send_message(
                    call.message.chat.id,
                    value.get('text', None),
                )
                send_message.append(sent_message)

                request_data = RequestSchedule(
                    transport_types=value.get('transport_types', None),
                    from_station=value.get('from_station', None),
                    to_station=value.get('to_station', None),
                )
                json_stations = await request_data.request_transport_between_stations()
                return json_stations.json()
    except Exception as error:
        sent_message = await bot.send_message(call.message.chat.id, error)
        send_message.append(sent_message)
        return None


class HandleUserRoute:
    result_route_stops: dict = {}
    selected_route_username: dict = {}


async def handler_thread(thread) -> str:
    for key, value in HandleUserRoute.result_route_stops.items():
        if key == thread[7:]:
            process_thread = Processing(value)
            return process_thread.detail_thread()


@bot.callback_query_handler(
    func=lambda call: call.data and call.data not in 'back',
)  # type: ignore
async def callback_handler_bus_route(call: types.CallbackQuery) -> None:
    try:
        if call.data.startswith('thread'):
            threads = await handler_thread(call.data)
            HandleUserRoute.selected_route_username[call.data[7:]] = (
                HandleUserRoute.result_route_stops[call.data[7:]]
            )
            await back_main(call.message, threads)
        elif call.data.startswith('schedule_'):
            select_route = HandleUserRoute.selected_route_username
            salt, login = encode_string(call.from_user.username)
            async with await create_database_session() as session:
                for key, value in select_route.items():
                    result_route = UserRoute(
                        username=login,
                        salt=salt,
                        thread=key,
                        number=value.get('number', None),
                        from_station=value.get('from').get('code'),
                        to_station=value.get('to').get('code'),
                    )
                    session.add(result_route)
                    await session.commit()
        else:
            await bot.delete_message(call.message.chat.id, call.message.id)
            json_data = await handler_request_transport(call)
            process = Processing(json_data)
            route_stops = await process.detail_transport()
            if not route_stops:
                raise KeyError('Яндекс не передал данные по маршрутам!')
            await selected_route(call.message, route_stops)
            HandleUserRoute.result_route_stops = route_stops
    except Exception as e:
        await bot.send_message(call.message.chat.id, f'Error: {e}')


@bot.callback_query_handler(
    func=lambda call: call.data in 'back',
)  # type: ignore
async def come_back_main(call: types.CallbackQuery) -> None:
    for message in send_message:
        try:
            await bot.delete_message(call.message.chat.id, message.message_id)
        except Exception as e:
            print(e)
            continue
    await select_transport_type(call.message)


def start_bot() -> Any:
    """Function for start telegram bot"""
    return bot.infinity_polling()
