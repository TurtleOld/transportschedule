from icecream import ic
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from transportschedule.schedule.telegram.config import bot


async def select_transport_type(message):
    keyboard = InlineKeyboardMarkup(row_width=1)
    bus = InlineKeyboardButton('Автобус', callback_data='bus')
    suburban = InlineKeyboardButton('Электричка', callback_data='suburban')
    keyboard.add(bus, suburban)
    await bot.send_message(
        message.chat.id,
        'Выбери тип транспорта',
        reply_markup=keyboard,
    )


async def selected_bus(message):
    keyboard = InlineKeyboardMarkup(row_width=1)
    bus_station_north = InlineKeyboardButton(
        'Автовокзал-Северный',
        callback_data='bus_station_north',
    )
    north_bus_station = InlineKeyboardButton(
        'Северный-Автовокзал',
        callback_data='north_bus_station',
    )
    keyboard.add(bus_station_north, north_bus_station)
    await bot.send_message(
        message.chat.id,
        'Выбери направление',
        reply_markup=keyboard,
    )


async def selected_route(message, route_info):
    keyboard = InlineKeyboardMarkup(row_width=3)
    for route in route_info:
        keyboard.add(
            InlineKeyboardButton(
                text=route,
                callback_data=' '.join(route.split()[:5]),
            )
        )
    await bot.send_message(
        message.chat.id,
        'Маршруты:',
        reply_markup=keyboard,
    )
