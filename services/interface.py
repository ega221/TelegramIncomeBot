"""Модуль, реализующий интерфейс сервиса"""

from model.messages import Message
from model.tg_update import Update
from model.user import User


class Service:
    async def initiate(self, upd: Update) -> Message:
        pass

    async def set_category(self, upd: Update) -> Message:
        pass

    async def set_date(self, upd: Update) -> Message:
        pass

    async def set_value(self, upd: Update) -> Message:
        pass

    async def save(self, upd: Update) -> Message:
        pass

    async def drop(self, upd: Update) -> Message:
        pass


class UserService:
    async def get(self, upd: Update) -> User:
        pass

    async def save(self, upd: Update) -> Message:
        pass
