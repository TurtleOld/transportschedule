"""Модуль разбора json данных."""

from typing import Any


class JsonParser:
    """
    Универсальный класс разбора json данных.

    АТРИБУТЫ:

    json_data: dict
        Словарь с данными.

    МЕТОДЫ:

    parse_json(json_data: dict, key: str) -> list[dict] | int | str | None
        Метод разбора json данных.
        Принимает словарь и ключ для поиска значения в переданном словаре.

    __get_value(dictionary, key) -> str | list | int | None)
        Приватный метод получения значений из словаря (json данных).
    """

    def __init__(self, json_data: dict[Any, Any]) -> None:
        """Метод-конструктор инициализирующий аргумент json_data."""
        self.json_data = json_data

    def parse_json(
        self,
        json_data,
        key: str,
        key2: str = None,
    ):
        """
        Метод разбора json данных.

        Принимает словарь и ключ для поиска значения в переданном словаре.

        АРГУМЕНТЫ:

        json_data: dict
            Принимает словарь.

        key: str
            Ключ для поиска в словаре.

        ВОЗВРАЩАЕТ:

        list[dict] | None
            Словарь внутри списка, либо None
        """
        return JsonParser.__get_value(self, json_data, key, key2)

    def __get_value(
        self,
        dictionary,
        key: str,
        key2: str = None,
    ):
        """
        Приватный метод получения значений из словаря (json данных).

        АРГУМЕНТЫ:

        dictionary: dict
            Принимает словарь данных.
        key: str
            Принимает ключ для поиска значения в словаре.

        ВОЗВРАЩАЕТ:

        str | list | int | None
            В зависимости от условий, может возвращать строку, список, число.
        """
        if isinstance(dictionary, dict):
            dict_value = dictionary.get(key, None)
            if key2 and isinstance(dict_value, dict):
                return dict_value.get(key2, None)
            return dict_value
        return None
