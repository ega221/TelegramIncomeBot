import asyncpg

from model.income import Income
from model.income_category import IncomeCategory

from model.user import User
from repository.interface import IncomeRepository


class IncomeRepositoryImpl(IncomeRepository):
    def __init__(self, pool: asyncpg.pool.Pool):
        self.pool = pool

    async def save(self, income: Income):
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO incomes(user_id, category_id, category_name, value, date) 
                VALUES($1, $2, $3, $4, $5)
            """,
                income.user_id,
                income.category_id,
                income.category_name,
                income.value,
                income.date,
            )

    async def get_income_by_id(self, income_id: int) -> Income | None:
        async with self.pool.acquire() as conn:
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
                    category_name=record["category_name"],
                    value=record["value"],
                    date=record["date"],
                )
            else:
                return None

    async def delete_income_by_id(self, income_id: int):
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                DELETE FROM incomes WHERE id = $1
            """,
                income_id,
            )

    async def get_incomes_by_user(self, user: User) -> list[Income]:
        async with self.pool.acquire() as conn:
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
                    category_name=record["category_name"],
                    value=record["value"],
                    date=record["date"],
                )
                incomes.append(income)
            return incomes

    async def get_incomes_by_category(self, category: IncomeCategory) -> list[Income]:
        async with self.pool.acquire() as conn:
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
                    category_name=record["category_name"],
                    value=record["value"],
                    date=record["date"],
                )
                incomes.append(income)
            return incomes
