import asyncpg

from model.income_category import IncomeCategory
from model.user import User

from repository.interface import IncomeCategoryRepository


class IncomeCategoryRepositoryImpl(IncomeCategoryRepository):
    def __init__(self, pool: asyncpg.pool.Pool):
        self.pool = pool

    async def save(self, income_category: IncomeCategory):
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                               INSERT INTO income_categories(user_id, category_name) VALUES($1, $2)
                           """,
                IncomeCategory.user_id,
                IncomeCategory.category_name,
            )

    async def get_category_by_id(self, category_id: int) -> IncomeCategory | None:
        async with self.pool.acquire() as conn:
            record = await conn.fetchrow(
                """
                    SELECT * FROM expense_categories WHERE id = $1
                """,
                category_id,
            )
            if record:
                return IncomeCategory(
                    id=record["id"],
                    user_id=record["user_id"],
                    category_name=record["category_name"],
                )
            else:
                return None

    async def delete_category_by_id(self, category_id: int):
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                DELETE FROM income_categories WHERE id = $1
            """,
                category_id,
            )

    async def get_categories_by_user(self, user: User) -> list[IncomeCategory]:
        async with self.pool.acquire() as conn:
            records = await conn.fetch(
                """
                SELECT * FROM income_categories WHERE user_id = $1
            """,
                user.id,
            )
            categories = []
            for record in records:
                category = IncomeCategory(
                    id=record["id"],
                    user_id=record["user_id"],
                    category_name=record["category_name"],
                )
                categories.append(category)
            return categories
