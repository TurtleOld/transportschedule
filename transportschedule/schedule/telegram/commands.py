import asyncio

import telebot
from aiohttp import web
from icecream import ic
from telebot import types

from transportschedule.schedule.process.processing import Processing
from transportschedule.schedule.request.request import RequestSchedule
from transportschedule.schedule.telegram.config import (
    bot,
    logger,
    WEBHOOK_URL_BASE,
    WEBHOOK_URL_PATH,
)
from transportschedule.schedule.telegram.keyboard import (
    select_transport_type,
    selected_bus,
    selected_route,
    selected_suburban,
    back_main,
)


# Process webhook calls
async def handle(request):
    if request.match_info.get('token') == bot.token:
        request_body_dict = await request.json()
        update = telebot.types.Update.de_json(request_body_dict)
        asyncio.ensure_future(bot.process_new_updates([update]))
        return web.Response()
    else:
        return web.Response(status=403)


# Remove webhook and closing session before exiting
async def shutdown(app):
    logger.info('Shutting down: removing webhook')
    await bot.remove_webhook()
    logger.info('Shutting down: closing session')
    await bot.close_session()


async def setup():
    # Remove webhook, it fails sometimes the set if there is a previous webhook
    logger.info('Starting up: removing old webhook')
    await bot.remove_webhook()
    # Set webhook
    logger.info('Starting up: setting webhook')
    await bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)
    app = web.Application()
    app.router.add_post('/{token}/', handle)
    app.on_cleanup.append(shutdown)
    return app


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
    process_thread = Processing(request)
    thread_info = process_thread.detail_thread()
    return thread_info


route_detail_info = None
json_data = None


@bot.callback_query_handler(
    func=lambda call: '_g24_' not in call.data and 'back' not in call.data,
)
async def callback_handler_bus_route(call):
    global route_detail_info
    global json_data
    await bot.delete_message(call.message.chat.id, call.message.id)
    json_data = await handler_request_transport(call)
    process = Processing(json_data)
    route_info, route_detail_info = process.detail_transport()
    await selected_route(call.message, route_info[:5], route_detail_info[:5])


@bot.callback_query_handler(
    func=lambda call: call.data in route_detail_info[:5],
)
async def route_detail_handler(call):
    await bot.delete_message(call.message.chat.id, call.message.id)
    threads = await handler_thread(call.data)
    await back_main(call.message, threads)


@bot.callback_query_handler(func=lambda call: call.data == 'back')
async def come_back(call):
    await bot.delete_message(call.message.chat.id, call.message.id - 4)
    await bot.delete_message(call.message.chat.id, call.message.id - 2)
    await bot.delete_message(call.message.chat.id, call.message.id)
    await select_transport_type(call.message)


async def start_bot():
    """Function for start telegram bot"""
    return await bot.infinity_polling()
