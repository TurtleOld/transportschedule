from telebot import types
from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)

from transportschedule.schedule.telegram.config import bot

send_message = []


async def keyboard_station(message: types.Message, stations) -> None:
    keyboard = InlineKeyboardMarkup(row_width=2)
    for key, value in stations.items():
        keyboard.add(
            InlineKeyboardButton(
                f'\u00A0\u00A0{str(value["station_type_name"]).capitalize()}: {value["title"]}\u00A0\u00A0',
                callback_data=key,
            )
        )
    sent_message = await bot.send_message(
        message.chat.id,
        '\u00A0\u00A0Остановки в радиусе 1 км:\u00A0\u00A0',
        reply_markup=keyboard,
    )
    send_message.append(sent_message)


def get_geo_location() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button = KeyboardButton(
        text='Отправить местоположение',
        request_location=True,
    )
    markup.add(button)
    return markup


async def select_transport_type(message: types.Message) -> None:
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
    sent_message = await bot.send_message(
        message.chat.id,
        '\u00A0\u00A0Выбери тип транспорта\u00A0\u00A0',
        reply_markup=keyboard,
    )
    send_message.append(sent_message)


async def selected_bus(message: types.Message) -> None:
    keyboard = InlineKeyboardMarkup(row_width=2)
    bus_station_north = InlineKeyboardButton(
        '\u00A0\u00A0Автовокзал - Северный\u00A0\u00A0',
        callback_data='bus_station_north',
    )
    north_bus_station = InlineKeyboardButton(
        '\u00A0\u00A0Северный - Автовокзал\u00A0\u00A0',
        callback_data='north_bus_station',
    )
    north_zhbi = InlineKeyboardButton(
        '\u00A0\u00A0Северный - Завод ЖБИ\u00A0\u00A0',
        callback_data='north_zhbi',
    )
    north_gymnasium = InlineKeyboardButton(
        '\u00A0\u00A0Северный - Гимназия № 5\u00A0\u00A0',
        callback_data='north_gymnasium',
    )
    north_vorobyovskaya = InlineKeyboardButton(
        '\u00A0\u00A0Северный - Воробьёвская улица\u00A0\u00A0',
        callback_data='north_vorobyovskaya',
    )
    vorobyovskaya_north = InlineKeyboardButton(
        '\u00A0\u00A0Воробьёвская улица - Северный\u00A0\u00A0',
        callback_data='vorobyovskaya_north',
    )
    keyboard.add(
        bus_station_north,
        north_bus_station,
        north_zhbi,
        north_gymnasium,
        north_vorobyovskaya,
        vorobyovskaya_north,
    )
    sent_message = await bot.send_message(
        message.chat.id,
        '\u00A0\u00A0Выбери направление\u00A0\u00A0',
        reply_markup=keyboard,
    )
    send_message.append(sent_message)


async def selected_suburban(message: types.Message) -> None:
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
    keyboard.add(
        InlineKeyboardButton(
            text='Вернуться в начало',
            callback_data='back',
        )
    )
    sent_message = await bot.send_message(
        message.chat.id,
        'Выбери направление',
        reply_markup=keyboard,
        parse_mode='HTML',
    )
    send_message.append(sent_message)


async def selected_route(
    message: types.Message,
    route_info: list[str],
    route_detail_info: list[str],
) -> None:
    keyboard = InlineKeyboardMarkup()
    if route_info:
        for route, detail in zip(route_info, route_detail_info):
            print(route)
            callback_data = 'thread ' + ' '.join(detail.split()[:5])
            keyboard.row(
                InlineKeyboardButton(
                    text=f'\u00A0\u00A0\u00A0{route}\u00A0\u00A0\u00A0',
                    callback_data=callback_data,
                )
            )
        keyboard.add(
            InlineKeyboardButton(
                text='Вернуться в начало',
                callback_data='back',
            )
        )
        sent_message = await bot.send_message(
            message.chat.id,
            'Маршруты:',
            reply_markup=keyboard,
        )
        send_message.append(sent_message)
    else:
        keyboard.add(
            InlineKeyboardButton(
                text='Вернуться в начало',
                callback_data='back',
            )
        )
        sent_message = await bot.send_message(
            message.chat.id,
            'На сегодня нет маршрутов...',
            reply_markup=keyboard,
        )
        send_message.append(sent_message)


async def back_main(message: types.Message, threads: str) -> None:
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            text='Вернуться в начало',
            callback_data='back',
        )
    )
    keyboard.add(
        InlineKeyboardButton(
            text='Запомнить маршрут',
            callback_data=f'schedule_{message.chat.id}',
        )
    )
    sent_message = await bot.send_message(
        message.chat.id,
        threads,
        reply_markup=keyboard,
    )
    send_message.append(sent_message)


async def back_from_routes(message: types.Message, routes: str) -> None:
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            text='Вернуться в начало',
            callback_data='back',
        )
    )
    sent_message = await bot.send_message(
        message.chat.id,
        routes,
        reply_markup=keyboard,
    )
    send_message.append(sent_message)
