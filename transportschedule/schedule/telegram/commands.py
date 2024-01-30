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


@bot.callback_query_handler(func=lambda call: True)
async def callback_handler_bus_route(call):
    await bot.delete_message(call.message.chat.id, call.message.id)
    json_data = await handler_request_transport(call)
    process = Processing(json_data)
    process_result = process.detail_transport()
    await selected_route(call.message, process_result[:5])


# @bot.callback_query_handler(
#     func=lambda call: call.data == 'yaroslavsky_railway_station_sergiev_posad'
# )
# async def callback_handler_suburban(call):
#     await bot.delete_message(call.message.chat.id, call.message.id)
#     await bot.send_message(
#         call.message.chat.id,
#         'Выбран маршрут: От Ярославского вокзала до Сергиев Посада',
#     )
#     request_data = RequestSchedule(
#         transport_types='suburban',
#         from_station=2000002,
#         to_station=9601389,
#     )
#     json_data = request_data.request_transport_between_stations()
#     process = Processing(json_data)
#     process_result = process.detail_transport()
#     await selected_route(call.message, process_result[:5])


async def start_bot():
    """Function for start telegram bot"""
    return await bot.infinity_polling()
