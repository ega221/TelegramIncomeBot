"""Модуль, реализующий сервис расходов"""

from model.expense import Expense
from services.interface import Service
from model.transient_expense import TransientExpense
from repository.interface import UserRepository, ExpenseCategoryRepository, ExpenseRepository
from datetime import datetime
from user_cache.interface import UserCache
from transaction.transaction_manager import TransactionManager


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

    async def initiate(self, telegram_id: int) -> TransientExpense:
        """Метод, инициализирующий временный Expense в кэше"""
        payload = TransientExpense(telegram_id=telegram_id)
        self.user_cache.update(telegram_id, payload)
        return payload

    async def set_category(self, telegram_id: int, category_name: str) -> TransientExpense:
        """Метод, устанавливающий для пользователя с заданным
        telegram_id нужную категорию
        """
        payload = self.user_cache.get(telegram_id)
        payload.category_name = category_name
        self.user_cache.update(telegram_id, payload)
        return payload

    async def set_date(self, telegram_id: int, date: datetime) -> TransientExpense:
        """Метод, устанавливающий дату для временного Expense
        для пользователя с заданным telegram_id
        """
        payload = self.user_cache.get(telegram_id)
        payload.date = date
        self.user_cache.update(telegram_id, payload)
        return payload

    async def set_value(self, telegram_id: int, value: int) -> TransientExpense:
        """Метод, устанавливающий размер временного Expense
        для пользователя с заданным telegram_id
        """
        payload = self.user_cache.get(telegram_id)
        payload.value = value
        self.user_cache.update(telegram_id, payload)
        return payload

    async def save(self, telegram_id: int) -> Expense:
        """Метод, сохраняющий временный Expense в базу данных
        с помощью соответствующих репозиториев. После успешной записи в бд,
        из кэша будет удалена запись с временным Expense
        """
        payload = self.user_cache.get(telegram_id)
        async with self.transaction_manager.get_connection() as conn:
            user_id = await self.user_repo.get_user_by_telegram_id(conn, telegram_id)
            user_categories = await self.expense_cat_repo.get_categories_by_user(conn, user_id)
            category_id = next((cat.id for cat in user_categories if cat.category_name == payload.category_name), None)
            value = payload.value
            date = payload.date
            expense = await self.expense_repo.save(conn, Expense(user_id, category_id, value, date))
        await self.drop(telegram_id)
        return expense

    async def drop(self, telegram_id: int) -> None:
        """Метод, удаляющий из кэша запись с временным Expense
        для пользователя с заданным telegram_id
        """
        self.user_cache.drop(telegram_id)
