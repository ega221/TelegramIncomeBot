"""Модуль, реализующий сервис расходов"""

from datetime import datetime
from decimal import Decimal

from model.expense import Expense
from model.messages import Message
from model.tg_update import Update
from model.transient_expense import TransientExpense
from repository.interface import (
    ExpenseCategoryRepository,
    ExpenseRepository,
    UserRepository,
)
from services.interface import Service
from transaction.transaction_manager import TransactionManager
from user_cache.interface import UserCache
from validators.category_validator import validate_category
from validators.date_validator import validate_date
from validators.number_validator import validate_number

DATETIME_SPLIT_CHAR = "-"


class ExpenseServiceImpl(Service):
    def __init__(
            self,
            user_cache: UserCache,
            transaction_manager: TransactionManager,
            user_repo: UserRepository,
            expense_cat_repo: ExpenseCategoryRepository,
            expense_repo: ExpenseRepository,
    ):
        self.user_cache = user_cache
        self.transaction_manager = transaction_manager
        self.user_repo = user_repo
        self.expense_cat_repo = expense_cat_repo
        self.expense_repo = expense_repo

    async def initiate(self, upd: Update) -> Message:
        """Метод, инициализирующий временный Expense в кэше"""
        payload = TransientExpense(telegram_id=upd.telegram_id)
        self.user_cache.update(upd.telegram_id, payload)
        async with self.transaction_manager.get_connection() as conn:
            user = await self.user_repo.get_user_by_telegram_id(conn, upd.telegram_id)
            categories = await self.expense_cat_repo.get_categories_by_user(conn, user)
            category_string = "\n".join([cat.category_name for cat in categories])
        return Message.INITIATE_INCOME + category_string

    @validate_category
    async def set_category(self, upd: Update) -> Message:
        """Метод, устанавливающий для пользователя с заданным
        telegram_id нужную категорию
        """
        payload = self.user_cache.get(upd.telegram_id)
        async with self.transaction_manager.get_connection() as conn:
            user = await self.user_repo.get_user_by_telegram_id(conn, upd.telegram_id)
            categories = await self.expense_cat_repo.get_categories_by_user(conn, user)
            category_string_list = [cat.category_name for cat in categories]
        if (upd.text in category_string_list):
            payload.category_name = upd.text
            self.user_cache.update(upd.telegram_id, payload)
            return Message.CATEGORY_SET
        else:
            raise ValueError("Такой категории нет")

    @validate_date
    async def set_date(self, upd: Update) -> Message:
        """Метод, устанавливающий дату для временного Expense
        для пользователя с заданным telegram_id
        """
        payload = self.user_cache.get(upd.telegram_id)
        payload.date = datetime.strptime(upd.text, '%d-%m-%Y')
        self.user_cache.update(upd.telegram_id, payload)
        return Message.DATE_SET

    @validate_number
    async def set_value(self, upd: Update) -> Message:
        """Метод, устанавливающий размер временного Expense
        для пользователя с заданным telegram_id
        """
        payload = self.user_cache.get(upd.telegram_id)
        payload.value = Decimal(upd.text)
        self.user_cache.update(upd.telegram_id, payload)
        return Message.VALUE_SET + "\n" + payload.to_string() + "\n" + Message.ADD_VALUE_MESSAGE

    async def save(self, upd: Update) -> Message:
        """Метод, сохраняющий временный Expense в базу данных
        с помощью соответствующих репозиториев. После успешной записи в бд,
        из кэша будет удалена запись с временным Expense
        """
        payload = self.user_cache.get(upd.telegram_id)
        async with self.transaction_manager.get_connection() as conn:
            user = await self.user_repo.get_user_by_telegram_id(conn, upd.telegram_id)
            user_categories = await self.expense_cat_repo.get_categories_by_user(conn, user)
            category_id = next((cat.id for cat in user_categories if cat.category_name == payload.category_name), None)
            value = payload.value
            date = payload.date
            await self.expense_repo.save(conn, Expense(user.id, category_id, value, date))
        await self.drop(upd)
        return Message.EXPENSE_SAVED

    async def drop(self, upd: Update) -> Message:
        """Метод, удаляющий из кэша запись с временным Expense
        для пользователя с заданным telegram_id
        """
        self.user_cache.drop(upd.telegram_id)
        return Message.EXPENSE_DROPPED
