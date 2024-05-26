from asyncpg import connection

from model.income import Income
from model.income_category import IncomeCategory

from model.user import User
from repository.interface import IncomeRepository


class IncomeRepositoryImpl(IncomeRepository):

    async def save(self, conn: connection, income: Income):
        result = await conn.fetchrow(
            """
            INSERT INTO incomes(user_id, category_id, value, date) 
            VALUES($1, $2, $3, $4) RETURNING id
            """,
            income.user_id,
            income.category_id,
            income.value,
            income.date,
        )
        income.id = result["id"]
        return income

    async def get_income_by_id(self, conn: connection, income_id: int) -> Income | None:
        record = await conn.fetchrow(
            """
            SELECT * FROM incomes WHERE id = $1
            """,
            income_id,
        )
        if record:
            return Income(
                id=record["id"],
                user_id=record["user_id"],
                category_id=record["category_id"],
                value=record["value"],
                date=record["date"],
            )
        else:
            return None

    async def delete_income_by_id(self, conn: connection, income_id: int):
        await conn.execute(
            """
            DELETE FROM incomes WHERE id = $1
            """,
            income_id,
        )

    async def get_incomes_by_user(self, conn: connection, user: User) -> list[Income]:
        records = await conn.fetch(
            """
            SELECT * FROM incomes WHERE user_id = $1
            """,
            user.id,
        )
        incomes = []
        for record in records:
            income = Income(
                id=record["id"],
                user_id=record["user_id"],
                category_id=record["category_id"],
                value=record["value"],
                date=record["date"],
            )
            incomes.append(income)
        return incomes

    async def get_incomes_by_category(self, conn: connection, category: IncomeCategory) -> list[Income]:
        records = await conn.fetch(
            """
            SELECT * FROM incomes WHERE category_id = $1
            """,
            category.id,
        )
        incomes = []
        for record in records:
            income = Income(
                id=record["id"],
                user_id=record["user_id"],
                category_id=record["category_id"],
                value=record["value"],
                date=record["date"],
            )
            incomes.append(income)
        return incomes
