from icecream import ic
from telebot import types

from transportschedule.schedule.process.processing import Processing
from transportschedule.schedule.request.request import RequestSchedule
from transportschedule.schedule.telegram.config import bot
from transportschedule.schedule.telegram.keyboard import (
    select_transport_type,
    selected_bus,
    selected_route,
    selected_suburban,
)


@bot.message_handler(commands=['select'])
async def handler_command_request(message: types.Message):
    await select_transport_type(message)


@bot.callback_query_handler(func=lambda call: call.data == 'bus')
async def callback_handler_bus(call):
    await bot.delete_message(call.message.chat.id, call.message.id)
    await bot.send_message(
        call.message.chat.id,
        'Выбран вид транспорта: Автобус',
    )
    await selected_bus(call.message)


@bot.callback_query_handler(func=lambda call: call.data == 'suburban')
async def callback_handler_suburban(call):
    await bot.delete_message(call.message.chat.id, call.message.id)
    await bot.send_message(
        call.message.chat.id,
        'Выбран вид транспорта: Электричка',
    )
    await selected_suburban(call.message)


async def handler_request_transport(call):
    if call.data == 'bus_station_north':
        await bot.send_message(
            call.message.chat.id,
            'Выбран маршрут: От Автовокзала Сергиев Посад до Северного посёлка',
        )
        request_data = RequestSchedule(
            transport_types='bus',
            from_station=9742908,
            to_station=9742891,
        )
        return request_data.request_transport_between_stations()
    elif call.data == 'north_bus_station':
        await bot.send_message(
            call.message.chat.id,
            'Выбран маршрут: От Северного посёлка до Автовокзала Сергиев Посад',
        )
        request_data = RequestSchedule(
            transport_types='bus',
            from_station=9742891,
            to_station=9742908,
        )
        return request_data.request_transport_between_stations()
    elif call.data == 'yaroslavsky_railway_station_sergiev_posad':
        await bot.send_message(
            call.message.chat.id,
            'Выбран маршрут: От Ярославского вокзала до Сергиев Посада',
        )
        request_data = RequestSchedule(
            transport_types='suburban',
            from_station=2000002,
            to_station=9601389,
        )
        return request_data.request_transport_between_stations()
    elif call.data == 'sergiev_posad_yaroslavsky_railway_station':
        await bot.send_message(
            call.message.chat.id,
            'Выбран маршрут: От Сергиев Посада до Ярославского вокзала',
        )
        request_data = RequestSchedule(
            transport_types='suburban',
            from_station=9601389,
            to_station=2000002,
        )
        return request_data.request_transport_between_stations()
    elif call.data == 'yaroslavsky_railway_station_podlipki':
        await bot.send_message(
            call.message.chat.id,
            'Выбран маршрут: От Ярославского вокзала до Подлипки-Дачные',
        )
        request_data = RequestSchedule(
            transport_types='suburban',
            from_station=2000002,
            to_station=9600691,
        )
        return request_data.request_transport_between_stations()
    elif call.data == 'podlipki_yaroslavsky_railway_station':
        await bot.send_message(
            call.message.chat.id,
            'Выбран маршрут: От Подлипки-Дачные до Ярославского вокзала',
        )
        request_data = RequestSchedule(
            transport_types='suburban',
            from_station=9600691,
            to_station=2000002,
        )
        return request_data.request_transport_between_stations()
    elif call.data == 'podlipki_mytischi':
        await bot.send_message(
            call.message.chat.id,
            'Выбран маршрут: От Подлипки-Дачные до Мытищи',
        )
        request_data = RequestSchedule(
            transport_types='suburban',
            from_station=9600691,
            to_station=9600681,
        )
        return request_data.request_transport_between_stations()
    elif call.data == 'mytischi_podlipki':
        await bot.send_message(
            call.message.chat.id,
            'Выбран маршрут: От Мытищи до Подлипки-Дачные',
        )
        request_data = RequestSchedule(
            transport_types='suburban',
            from_station=9600681,
            to_station=9600691,
        )
        return request_data.request_transport_between_stations()
    elif call.data == 'yaroslavsky_railway_station_mytischi':
        await bot.send_message(
            call.message.chat.id,
            'Выбран маршрут: От Ярославского вокзала до Мытищи',
        )
        request_data = RequestSchedule(
            transport_types='suburban',
            from_station=2000002,
            to_station=9600681,
        )
        return request_data.request_transport_between_stations()
    elif call.data == 'sergiev_posad_mytischi':
        await bot.send_message(
            call.message.chat.id,
            'Выбран маршрут: От Сергиев Посада до Мытищи',
        )
        request_data = RequestSchedule(
            transport_types='suburban',
            from_station=9601389,
            to_station=9600681,
        )
        return request_data.request_transport_between_stations()
    elif call.data == 'mytischi_sergiev_posad':
        await bot.send_message(
            call.message.chat.id,
            'Выбран маршрут: От Мытищи до Сергиев Посада',
        )
        request_data = RequestSchedule(
            transport_types='suburban',
            from_station=9600681,
            to_station=9601389,
        )
        return request_data.request_transport_between_stations()
    elif call.data == 'black_serp_molot':
        await bot.send_message(
            call.message.chat.id,
            'Выбран маршрут: От Чёрное до Серп и Молот',
        )
        request_data = RequestSchedule(
            transport_types='suburban',
            from_station=9601301,
            to_station=9601796,
        )
        return request_data.request_transport_between_stations()
    elif call.data == 'serp_molot_black':
        await bot.send_message(
            call.message.chat.id,
            'Выбран маршрут: От Серп и Молот до Чёрное',
        )
        request_data = RequestSchedule(
            transport_types='suburban',
            from_station=9601796,
            to_station=9601301,
        )
        return request_data.request_transport_between_stations()


async def handler_thread(call, threads, json_data):
    process_thread = Processing(json_data)
    station_info = process_thread.get_transport_route()
    from_station = station_info[0]
    to_station = station_info[2]
    for thread in threads:
        request = RequestSchedule(
            uid=thread,
            from_station=from_station,
            to_station=to_station,
        )
        thread_info = request.request_thread_transport_route()



@bot.callback_query_handler(func=lambda call: True)
async def callback_handler_bus_route(call):
    await bot.delete_message(call.message.chat.id, call.message.id)
    json_data = await handler_request_transport(call)
    process = Processing(json_data)
    route_info, route_detail_info = process.detail_transport()
    await selected_route(call.message, route_info[:5], route_detail_info[:5])
    await handler_thread(call, route_detail_info[:5], json_data)


async def start_bot():
    """Function for start telegram bot"""
    return await bot.infinity_polling()
