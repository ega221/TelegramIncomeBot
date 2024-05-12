import asyncpg

from model.expense import Expense
from model.expense_category import ExpenseCategory

from model.user import User
from repository.interface import ExpenseRepository


class ExpenseRepositoryImpl(ExpenseRepository):

    def __init__(self, pool: asyncpg.pool.Pool):
        self.pool = pool

    async def save(self, expense: Expense):
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO expenses(user_id, category_id, category_name, value, date) 
                VALUES($1, $2, $3, $4, $5)
            """,
                expense.user_id,
                expense.category_id,
                expense.category_name,
                expense.value,
                expense.date,
            )

    async def get_expense_by_id(self, expense_id: int) -> Expense | None:
        async with self.pool.acquire() as conn:
            record = await conn.fetchrow(
                """
                    SELECT * FROM expenses WHERE id = $1
                """,
                expense_id,
            )
            if record:
                return Expense(
                    id=record["id"],
                    user_id=record["user_id"],
                    category_id=record["category_id"],
                    category_name=record["category_name"],
                    value=record["value"],
                    date=record["date"],
                )
            else:
                return None

    async def delete_expense_by_id(self, expense_id: int):
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                DELETE FROM expenses WHERE id = $1
            """,
                expense_id,
            )

    async def get_expenses_by_user(self, user: User) -> list[Expense]:
        async with self.pool.acquire() as conn:
            records = await conn.fetch(
                """
                SELECT * FROM expenses WHERE user_id = $1
            """,
                user.id,
            )
            expenses = []
            for record in records:
                expense = Expense(
                    id=record["id"],
                    user_id=record["user_id"],
                    category_id=record["category_id"],
                    category_name=record["category_name"],
                    value=record["value"],
                    date=record["date"],
                )
                expenses.append(expense)
            return expenses

    async def get_expenses_by_category(
        self, category: ExpenseCategory
    ) -> list[Expense]:
        async with self.pool.acquire() as conn:
            records = await conn.fetch(
                """
                SELECT * FROM expenses WHERE category_id = $1
            """,
                category.id,
            )
            expenses = []
            for record in records:
                expense = Expense(
                    id=record["id"],
                    user_id=record["user_id"],
                    category_id=record["category_id"],
                    category_name=record["category_name"],
                    value=record["value"],
                    date=record["date"],
                )
                expenses.append(expense)
            return expenses
