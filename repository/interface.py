from typing import Protocol

from model.expense import Expense
from model.expense_category import ExpenseCategory
from model.income import Income
from model.income_category import IncomeCategory
from model.user import User


class UserRepository(Protocol):
    def save(self, user: User):
        pass

    def get_user_by_id(self, user_id: int) -> User:
        pass

    def delete_user_by_id(self, user_id: int):
        pass


class ExpenseCategoryRepository(Protocol):
    def save(self, expense_category: ExpenseCategory):
        pass

    def get_category_by_id(self, category_id: int) -> ExpenseCategory:
        pass

    def delete_category_by_id(self, category_id: int):
        pass

    def get_categories_by_user(self, user: User) -> list[ExpenseCategory]:
        pass


class IncomeCategoryRepository(Protocol):
    def save(self, income_category: IncomeCategory):
        pass

    def get_category_by_id(self, category_id: int) -> IncomeCategory:
        pass

    def delete_category_by_id(self, category_id: int):
        pass

    def get_categories_by_user(self, user: User) -> list[IncomeCategory]:
        pass


class ExpenseRepository(Protocol):
    def save(self, expense: Expense):
        pass

    def get_expense_by_id(self, expense_id: int) -> Expense:
        pass

    def delete_expense_by_id(self, expense_id: int):
        pass

    def get_expenses_by_user(self, user: User) -> list[Expense]:
        pass

    def get_expenses_by_category(self, category: ExpenseCategory) -> list[Expense]:
        pass


class IncomeRepository(Protocol):
    def save(self, income: Income):
        pass

    def get_income_by_id(self, income_id: int) -> Income:
        pass

    def delete_income_by_id(self, income_id: int):
        pass

    def get_incomes_by_user(self, user: User) -> list[Expense]:
        pass

    def get_incomes_by_category(self, category: ExpenseCategory) -> list[Expense]:
        pass
