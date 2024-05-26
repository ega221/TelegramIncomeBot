from asyncpg import connection

from model.expense import Expense
from model.expense_category import ExpenseCategory

from model.user import User
from repository.interface import ExpenseRepository


class ExpenseRepositoryImpl(ExpenseRepository):
    async def save(self, conn: connection, expense: Expense):
        result = await conn.execute(
            """
            INSERT INTO expenses(user_id, category_id, value, date) 
            VALUES($1, $2, $3, $4) RETURNING id
            """,
            expense.user_id,
            expense.category_id,
            expense.value,
            expense.date,
        )
        expense.id = result["id"]
        return expense

    async def get_expense_by_id(self, conn: connection, expense_id: int) -> Expense | None:
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
                value=record["value"],
                date=record["date"],
            )
        else:
            return None

    async def delete_expense_by_id(self, conn: connection, expense_id: int):
        await conn.execute(
            """
            DELETE FROM expenses WHERE id = $1
            """,
            expense_id,
        )

    async def get_expenses_by_user(self, conn: connection, user: User) -> list[Expense]:
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
                value=record["value"],
                date=record["date"],
            )
            expenses.append(expense)
        return expenses

    async def get_expenses_by_category(self, conn: connection, category: ExpenseCategory) -> list[Expense]:
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
                value=record["value"],
                date=record["date"],
            )
            expenses.append(expense)
        return expenses
