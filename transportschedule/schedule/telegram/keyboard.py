import datetime

from icecream import ic
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from transportschedule.schedule.telegram.config import bot


async def select_transport_type(message):
    keyboard = InlineKeyboardMarkup(row_width=1)
    bus = InlineKeyboardButton(
        '\u00A0\u00A0Автобус\u00A0\u00A0',
        callback_data='bus',
    )
    suburban = InlineKeyboardButton(
        '\u00A0\u00A0Электричка\u00A0\u00A0',
        callback_data='suburban',
    )
    keyboard.add(bus, suburban)
    await bot.send_message(
        message.chat.id,
        '\u00A0\u00A0Выбери тип транспорта\u00A0\u00A0',
        reply_markup=keyboard,
    )


async def selected_bus(message):
    keyboard = InlineKeyboardMarkup(row_width=1)
    bus_station_north = InlineKeyboardButton(
        '\u00A0\u00A0Автовокзал - Северный\u00A0\u00A0',
        callback_data='bus_station_north',
    )
    north_bus_station = InlineKeyboardButton(
        '\u00A0\u00A0Северный - Автовокзал\u00A0\u00A0',
        callback_data='north_bus_station',
    )
    keyboard.add(bus_station_north, north_bus_station)
    await bot.send_message(
        message.chat.id,
        '\u00A0\u00A0Выбери направление\u00A0\u00A0',
        reply_markup=keyboard,
    )


async def selected_suburban(message):
    keyboard = InlineKeyboardMarkup(row_width=2)
    yaroslavsky_railway_station_sergiev_posad = InlineKeyboardButton(
        '\u00A0\u00A0Ярославкий вокзал - Сергиев Посад\u00A0\u00A0',
        callback_data='yaroslavsky_railway_station_sergiev_posad',
    )
    sergiev_posad_yaroslavsky_railway_station = InlineKeyboardButton(
        '\u00A0\u00A0Сергиев Посад - Ярославкий вокзал\u00A0\u00A0',
        callback_data='sergiev_posad_yaroslavsky_railway_station',
    )

    yaroslavsky_railway_station_podlipki = InlineKeyboardButton(
        '\u00A0\u00A0Ярославкий вокзал - Подлипки-Дачные\u00A0\u00A0',
        callback_data='yaroslavsky_railway_station_podlipki',
    )
    podlipki_yaroslavsky_railway_station = InlineKeyboardButton(
        '\u00A0\u00A0Подлипки-Дачные - Ярославкий вокзал\u00A0\u00A0',
        callback_data='podlipki_yaroslavsky_railway_station',
    )

    podlipki_mytischi = InlineKeyboardButton(
        '\u00A0\u00A0Подлипки-Дачные - Мытищи\u00A0\u00A0',
        callback_data='podlipki_mytischi',
    )
    mytischi_podlipki = InlineKeyboardButton(
        '\u00A0\u00A0Мытищи - Подлипки-Дачные\u00A0\u00A0',
        callback_data='mytischi_podlipki',
    )
    yaroslavsky_railway_station_mytischi = InlineKeyboardButton(
        '\u00A0\u00A0Ярославкий вокзал - Мытищи\u00A0\u00A0',
        callback_data='yaroslavsky_railway_station_mytischi',
    )

    sergiev_posad_mytischi = InlineKeyboardButton(
        '\u00A0\u00A0Сергиев Посад - Мытищи\u00A0\u00A0',
        callback_data='sergiev_posad_mytischi',
    )

    mytischi_sergiev_posad = InlineKeyboardButton(
        '\u00A0\u00A0Мытищи - Сергиев Посад\u00A0\u00A0',
        callback_data='mytischi_sergiev_posad',
    )

    black_serp_molot = InlineKeyboardButton(
        '\u00A0\u00A0Чёрное - Серп и Молот\u00A0\u00A0',
        callback_data='black_serp_molot',
    )
    serp_molot_black = InlineKeyboardButton(
        '\u00A0\u00A0Серп и Молот - Чёрное\u00A0\u00A0',
        callback_data='serp_molot_black',
    )
    keyboard.row(
        yaroslavsky_railway_station_sergiev_posad,
        sergiev_posad_yaroslavsky_railway_station,
    )
    keyboard.add(
        yaroslavsky_railway_station_podlipki,
        podlipki_yaroslavsky_railway_station,
        podlipki_mytischi,
        mytischi_podlipki,
        yaroslavsky_railway_station_mytischi,
        sergiev_posad_mytischi,
        mytischi_sergiev_posad,
        black_serp_molot,
        serp_molot_black,
    )
    await bot.send_message(
        message.chat.id,
        'Выбери направление',
        reply_markup=keyboard,
        parse_mode='HTML',
    )


async def selected_route(message, route_info, route_detail_info):
    keyboard = InlineKeyboardMarkup()
    for route, detail in zip(route_info, route_detail_info):
        callback_data = ' '.join(detail.split()[:5])
        keyboard.row(
            InlineKeyboardButton(
                text=f'\u00A0\u00A0\u00A0{route}\u00A0\u00A0\u00A0',
                callback_data=callback_data,
            )
        )
    await bot.send_message(
        message.chat.id,
        'Маршруты:',
        reply_markup=keyboard,
    )
