"""Модуль, реализующий пользовательский сервис"""

from model.user import User
from model.response_templates import Update
from model.messages import Message
from services.interface import Service
from repository.interface import UserRepository
from transaction.transaction_manager import TransactionManager


class UserServiceImpl(Service):
    def __init__(self, transaction_manager: TransactionManager, user_repo: UserRepository):
        self.transaction_manager = transaction_manager
        self.user_repo = user_repo

    async def get(self, upd: Update) -> User:
        """Метод, возвращающий пользователя из базы данных по его telegram_id"""
        async with self.transaction_manager.get_connection() as conn:
            return await self.user_repo.get_user_by_telegram_id(conn, upd.telegram_id)

    async def save(self, upd: Update) -> Message:
        """Метод, сохраняющий пользователя в базе данных"""
        async with self.transaction_manager.get_connection() as conn:
            user = self.user_repo.get_user_by_telegram_id(conn, upd.update_id)
            if not user:
                await self.user_repo.save(conn, User(upd.update_id))
        return Message.GREETING
