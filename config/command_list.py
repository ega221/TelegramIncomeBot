"""Файл, содержащий enum со всеми командами"""

from enum import StrEnum


class CommandsEnum(StrEnum):
    """str enum, который хранит в себе все команды"""

    make_income = "/make_income"
    make_expense = "/make_expense"
    get_income_categories = "/get_income_categories"
    get_expense_categories = "/get_expense_categories"

    @classmethod
    def get_commands(cls):
        """Метод возвращает список из всех доступных команд"""
        return [value.value for value in cls]
