"""Файл, содержащий enum со всеми командами"""

from enum import StrEnum


class StatusEnum(StrEnum):
    """str enum, который хранит в себе все команды"""

    idle = "IDLE"

    @classmethod
    def get_status(cls):
        """Метод возвращает список из всех доступных команд"""
        return [value.value for value in cls]
