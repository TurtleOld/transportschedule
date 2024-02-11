import json
import os
import re
from typing import Any, Dict
from telebot import types
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

route_detail_info = None
json_data = None
route_stops = None
route_duration = None
route_arrival = None


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
    await select_transport_type(message)


@bot.callback_query_handler(
    func=lambda call: re.match(r's\d+', call.data),
)  # type: ignore
async def handle_stations(call: types.CallbackQuery) -> None:
    transport_route = ''
    station_response = RequestSchedule(current_station=call.data)
    result_station_response = await station_response.request_flight_schedule_station()
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


@bot.callback_query_handler(
    func=lambda call: call.data == 'bus',
)  # type: ignore
async def callback_handler_bus(call: types.CallbackQuery) -> None:
    await bot.delete_message(call.message.chat.id, call.message.id)
    sent_message = await bot.send_message(
        call.message.chat.id,
        'Выбран вид транспорта: Автобус',
    )
    send_message.append(sent_message)
    await selected_bus(call.message)


@bot.callback_query_handler(
    func=lambda call: call.data == 'suburban',
)  # type: ignore
async def callback_handler_suburban(call: types.CallbackQuery) -> None:
    await bot.delete_message(call.message.chat.id, call.message.id)
    sent_message = await bot.send_message(
        call.message.chat.id,
        'Выбран вид транспорта: Электричка',
    )
    send_message.append(sent_message)
    await selected_suburban(call.message)


async def handler_request_transport(
    call: types.CallbackQuery,
) -> Dict[str, str | int] | None:
    try:
        path = '../transportschedule/schedule/telegram/routes.json'
        json_file = os.path.abspath(path)
        with open(json_file, 'r') as route_file:
            json_route = json.load(route_file)

        for key, value in json_route.items():
            if key == call.data:
                sent_message = await bot.send_message(
                    call.message.chat.id, value.get('text', None)
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
        sent_message = await bot.send_message(
            call.message.chat.id,
            error,
        )
        send_message.append(sent_message)
        return None


async def handler_thread(thread: str) -> str:
    process_thread = Processing(json_data)
    station_info = process_thread.get_transport_route()
    from_station = station_info[0]
    to_station = station_info[2]
    request = RequestSchedule(
        uid=thread,
        from_station=from_station,
        to_station=to_station,
    )
    result_request = await request.request_thread_transport_route()
    json_data_thread = result_request.json()
    process_thread = Processing(
        json_data_thread,
        route_stops,
        route_duration,
        route_arrival,
    )
    return process_thread.detail_thread()


@bot.callback_query_handler(
    func=lambda call: call.data.startswith('thread'),
)  # type: ignore
async def route_detail_handler(call: types.CallbackQuery) -> None:
    await bot.delete_message(call.message.chat.id, call.message.id)
    threads = await handler_thread(call.data[7:])
    await back_main(call.message, threads)


@bot.callback_query_handler(
    func=lambda call: call.data and call.data not in 'back',
)  # type: ignore
async def callback_handler_bus_route(call: types.CallbackQuery) -> None:
    global route_detail_info
    global json_data
    global route_stops
    global route_duration
    global route_arrival
    await bot.delete_message(call.message.chat.id, call.message.id)
    json_data = await handler_request_transport(call)
    process = Processing(json_data)
    (
        route_info,
        route_detail_info,
        route_stops,
        route_duration,
        route_arrival,
    ) = process.detail_transport()
    await selected_route(call.message, route_info[:7], route_detail_info[:7])


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


async def start_bot() -> Any:
    """Function for start telegram bot"""
    return await bot.infinity_polling()
