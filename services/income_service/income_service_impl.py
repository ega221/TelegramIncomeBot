"""Модуль, реализующий сервис доходов"""

from model.income import Income
from model.tg_update import Update
from model.messages import Message
from decimal import Decimal
from datetime import datetime
from model.transient_income import TransientIncome
from services.interface import Service
from repository.interface import UserRepository, IncomeCategoryRepository, IncomeRepository
from user_cache.interface import UserCache
from transaction.transaction_manager import TransactionManager
from validators.category_validator import validate_category
from validators.date_validator import validate_date
from validators.number_validator import validate_number

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
        self.income_cat_repo = income_cat_repo
        self.income_repo = income_repo

    async def initiate(self, upd: Update = None) -> Message:
        """Метод, инициализирующий временный Income в кэше"""
        payload = TransientIncome(telegram_id=upd.telegram_id)
        self.user_cache.update(upd.telegram_id, payload)
        async with self.transaction_manager.get_connection() as conn:
            user = await self.user_repo.get_user_by_telegram_id(conn, upd.telegram_id)
            categories = await self.income_cat_repo.get_categories_by_user(conn, user)
            category_string = "\n".join([cat.category_name for cat in categories])
        return Message.INITIATE_INCOME + category_string

    @validate_category
    async def set_category(self, upd: Update = None) -> Message:
        """Метод, устанавливающий для пользователя с заданным
        telegram_id нужную категорию
        """
        payload = self.user_cache.get(upd.telegram_id)
        async with self.transaction_manager.get_connection() as conn:
            user = await self.user_repo.get_user_by_telegram_id(conn, upd.telegram_id)
            categories = await self.income_cat_repo.get_categories_by_user(conn, user)
            category_string_list = [cat.category_name for cat in categories]
        if (upd.text in category_string_list):
            payload.category_name = upd.text
            self.user_cache.update(upd.telegram_id, payload)
            return Message.CATEGORY_SET
        else:
            raise ValueError("Такой категории нет")

    @validate_date
    async def set_date(self, upd: Update = None) -> Message:
        """Метод, устанавливающий дату для временного Income
        для пользователя с заданным telegram_id
        """
        payload = self.user_cache.get(upd.telegram_id)
        payload.date = datetime.strptime(upd.text, '%d-%m-%Y')
        self.user_cache.update(upd.telegram_id, payload)
        return Message.DATE_SET

    @validate_number
    async def set_value(self, upd: Update = None) -> Message:
        """Метод, устанавливающий размер временного Income
        для пользователя с заданным telegram_id
        """
        payload = self.user_cache.get(upd.telegram_id)
        payload.value = Decimal(upd.text)
        self.user_cache.update(upd.telegram_id, payload)
        return Message.VALUE_SET + "\n" + payload.to_string() + "\n" + Message.ADD_VALUE_MESSAGE

    async def save(self, upd: Update = None) -> Message:
        """Метод, сохраняющий временный Income в базу данных
        с помощью соответствующих репозиториев. После успешной записи в бд,
        из кэша будет удалена запись с временным Income
        """
        payload = self.user_cache.get(upd.telegram_id)
        async with self.transaction_manager.get_connection() as conn:
            user = await self.user_repo.get_user_by_telegram_id(conn, upd.telegram_id)
            user_categories = await self.income_cat_repo.get_categories_by_user(conn, user)
            category_id = next((cat.id for cat in user_categories if cat.category_name == payload.category_name), None)
            value = payload.value
            date = payload.date
            await self.income_repo.save(conn, Income(user.id, category_id, value, date))
        await self.drop(upd)
        return Message.INCOME_SAVED

    async def drop(self, upd: Update = None) -> Message:
        """Метод, удаляющий из кэша запись с временным Income
        для пользователя с заданным telegram_id"""
        self.user_cache.drop(upd.telegram_id)
        return Message.INCOME_DROPPED
