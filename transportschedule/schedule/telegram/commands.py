from telebot import types

from transportschedule import constants
from transportschedule.schedule.process.processing import Processing
from transportschedule.schedule.request.request import RequestSchedule
from transportschedule.schedule.telegram.config import bot
from transportschedule.schedule.telegram.keyboard import (
    select_transport_type,
    selected_bus,
    selected_route,
    selected_suburban,
    back_main,
)

route_detail_info = None
json_data = None
route_stops = None


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
            from_station=constants.BUS_STATION_SERGIEV_POSAD,
            to_station=constants.BUS_STOP_NORTH_VILLAGE,
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
    elif call.data == 'north_zhbi':
        await bot.send_message(
            call.message.chat.id,
            'Выбран маршрут: От Северного посёлка до Завода ЖБИ',
        )
        request_data = RequestSchedule(
            transport_types='bus',
            from_station=9742891,
            to_station=9742916,
        )
        return request_data.request_transport_between_stations()
    elif call.data == 'north_gymnasium':
        await bot.send_message(
            call.message.chat.id,
            'Выбран маршрут: От Северного посёлка до Гимназии №5',
        )
        request_data = RequestSchedule(
            transport_types='bus',
            from_station=9742891,
            to_station=9742870,
        )
        return request_data.request_transport_between_stations()
    elif call.data == 'north_vorobyovskaya':
        await bot.send_message(
            call.message.chat.id,
            'Выбран маршрут: От Северного посёлка до Воробьёвской улицы',
        )
        request_data = RequestSchedule(
            transport_types='bus',
            from_station=9742891,
            to_station=9742900,
        )
        return request_data.request_transport_between_stations()
    elif call.data == 'vorobyovskaya_north':
        await bot.send_message(
            call.message.chat.id,
            'Выбран маршрут: От Воробьёвской улицы до Северного посёлка',
        )
        request_data = RequestSchedule(
            transport_types='bus',
            from_station=9742900,
            to_station=9742891,
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


async def handler_thread(thread):
    process_thread = Processing(json_data)
    station_info = process_thread.get_transport_route()
    from_station = station_info[0]
    to_station = station_info[2]
    request = RequestSchedule(
        uid=thread,
        from_station=from_station,
        to_station=to_station,
    )
    request = request.request_thread_transport_route()
    process_thread = Processing(request, route_stops)
    thread_info = process_thread.detail_thread()
    return thread_info


@bot.callback_query_handler(func=lambda call: call.data.startswith('thread'))
async def route_detail_handler(call):
    await bot.delete_message(call.message.chat.id, call.message.id)
    threads = await handler_thread(call.data[7:])
    await back_main(call.message, threads)


@bot.callback_query_handler(
    func=lambda call: call.data and call.data not in 'back',
)
async def callback_handler_bus_route(call):
    global route_detail_info
    global json_data
    global route_stops
    await bot.delete_message(call.message.chat.id, call.message.id)
    json_data = await handler_request_transport(call)
    process = Processing(json_data)
    route_info, route_detail_info, route_stops = process.detail_transport()
    await selected_route(call.message, route_info[:5], route_detail_info[:5])


@bot.callback_query_handler(func=lambda call: call.data in 'back')
async def come_back_main(call):
    await bot.delete_message(call.message.chat.id, call.message.id - 4)
    await bot.delete_message(call.message.chat.id, call.message.id - 2)
    await bot.delete_message(call.message.chat.id, call.message.id)
    await select_transport_type(call.message)


async def start_bot():
    """Function for start telegram bot"""
    return await bot.infinity_polling()
