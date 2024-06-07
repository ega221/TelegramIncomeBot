"""Модуль, реализующий сервис доходов"""

from model.income import Income
from model.response_templates import Update
from model.messages import Message
from decimal import Decimal
from datetime import datetime
from model.transient_income import TransientIncome
from services.interface import Service
from repository.interface import UserRepository, IncomeCategoryRepository, IncomeRepository
from user_cache.interface import UserCache
from transaction.transaction_manager import TransactionManager

DATETIME_SPLIT_CHAR = "-"


class IncomeServiceImpl(Service):
    def __init__(
            self,
            user_cache: UserCache,
            transaction_manager: TransactionManager,
            user_repo: UserRepository,
            income_cat_repo: IncomeCategoryRepository,
            income_repo: IncomeRepository,
    ):
        self.user_cache = user_cache
        self.transaction_manager = transaction_manager
        self.user_repo = user_repo
        self.expense_cat_repo = income_cat_repo
        self.expense_repo = income_repo

    async def initiate(self, upd: Update) -> Message:
        """Метод, инициализирующий временный Income в кэше"""
        payload = TransientIncome(telegram_id=upd.telegram_id)
        self.user_cache.update(upd.telegram_id, payload)
        return Message.INITIATE_INCOME

    async def set_category(self, upd: Update) -> Message:
        """Метод, устанавливающий для пользователя с заданным
        telegram_id нужную категорию
        """
        payload = self.user_cache.get(upd.telegram_id)
        payload.category_name = upd.text
        self.user_cache.update(upd.telegram_id, payload)
        return Message.CATEGORY_SET

    async def set_date(self, upd: Update) -> Message:
        """Метод, устанавливающий дату для временного Income
        для пользователя с заданным telegram_id
        """
        payload = self.user_cache.get(upd.telegram_id)
        payload.date = datetime(*upd.text.split(DATETIME_SPLIT_CHAR))
        self.user_cache.update(upd.telegram_id, payload)
        return Message.DATE_SET

    async def set_value(self, upd: Update) -> Message:
        """Метод, устанавливающий размер временного Income
        для пользователя с заданным telegram_id
        """
        payload = self.user_cache.get(upd.telegram_id)
        payload.value = Decimal(upd.text)
        self.user_cache.update(upd.telegram_id, payload)
        return Message.VALUE_SET

    async def save(self, upd: Update) -> Message:
        """Метод, сохраняющий временный Income в базу данных
        с помощью соответствующих репозиториев. После успешной записи в бд,
        из кэша будет удалена запись с временным Income
        """
        payload = self.user_cache.get(upd.telegram_id)
        async with self.transaction_manager.get_connection() as conn:
            user = await self.user_repo.get_user_by_telegram_id(conn, upd.telegram_id)
            user_categories = await self.expense_cat_repo.get_categories_by_user(conn, user)
            category_id = next((cat.id for cat in user_categories if cat.category_name == payload.category_name), None)
            value = payload.value
            date = payload.date
            await self.expense_repo.save(conn, Income(user.id, category_id, value, date))
        await self.drop(upd)
        return Message.INCOME_SAVED

    async def drop(self, upd: Update) -> Message:
        """Метод, удаляющий из кэша запись с временным Income
        для пользователя с заданным telegram_id"""
        self.user_cache.drop(upd.telegram_id)
        return Message.INCOME_DROPPED
