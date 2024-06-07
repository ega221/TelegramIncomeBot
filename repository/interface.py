from typing import Protocol
from model.expense import Expense
from model.expense_category import ExpenseCategory
from model.income import Income
from model.income_category import IncomeCategory
from model.user import User
from typing import TypeAlias
from asyncpg import connection

SupportedConnection: TypeAlias = connection


class UserRepository(Protocol):
    async def save(self, conn: SupportedConnection, user: User) -> User:
        pass

    async def get_user_by_id(self, conn: SupportedConnection, user_id: int) -> User:
        pass

    async def get_user_by_telegram_id(self, conn: connection, update_id: int) -> User:
        pass

    async def delete_user_by_id(self, conn: SupportedConnection, user_id: int):
        pass


class ExpenseCategoryRepository(Protocol):
    async def save(self, conn: SupportedConnection, expense_category: ExpenseCategory) -> ExpenseCategory:
        pass

    async def get_category_by_id(self, conn: SupportedConnection, category_id: int) -> ExpenseCategory:
        pass

    async def delete_category_by_id(self, conn: SupportedConnection, category_id: int):
        pass

    async def get_categories_by_user(self, conn: SupportedConnection, user: User) -> list[ExpenseCategory]:
        pass


class IncomeCategoryRepository(Protocol):
    async def save(self, conn: SupportedConnection, income_category: IncomeCategory) -> IncomeCategory:
        pass

    async def get_category_by_id(self, conn: SupportedConnection, category_id: int) -> IncomeCategory:
        pass

    async def delete_category_by_id(self, conn: SupportedConnection, category_id: int):
        pass

    async def get_categories_by_user(self, conn: SupportedConnection, user: User) -> list[IncomeCategory]:
        pass


class ExpenseRepository(Protocol):
    async def save(self, conn: SupportedConnection, expense: Expense) -> Expense:
        pass

    async def get_expense_by_id(self, conn: SupportedConnection, expense_id: int) -> Expense:
        pass

    async def delete_expense_by_id(self, conn: SupportedConnection, expense_id: int):
        pass

    async def get_expenses_by_user(self, conn: SupportedConnection, user: User) -> list[Expense]:
        pass

    async def get_expenses_by_category(self, conn: SupportedConnection, category: ExpenseCategory) -> list[Expense]:
        pass


class IncomeRepository(Protocol):
    async def save(self, conn: SupportedConnection, income: Income) -> Income:
        pass

    async def get_income_by_id(self, conn: SupportedConnection, income_id: int) -> Income:
        pass

    async def delete_income_by_id(self, conn: SupportedConnection, income_id: int):
        pass

    async def get_incomes_by_user(self, conn: SupportedConnection, user: User) -> list[Income]:
        pass

    async def get_incomes_by_category(self, conn: SupportedConnection, category: Income) -> list[Income]:
        pass
