"""Модуль, реализующий интерфейс сервиса"""

from model.response_templates import Update
from model.user import User
from model.messages import Message


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
