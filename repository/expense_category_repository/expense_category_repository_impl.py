import asyncpg

from model.expense_category import ExpenseCategory
from model.user import User

from repository.interface import ExpenseCategoryRepository


class ExpenseCategoryRepositoryImpl(ExpenseCategoryRepository):

    def __init__(self, pool: asyncpg.pool.Pool):
        self.pool = pool

    async def save(self, expense_category: ExpenseCategory):
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                               INSERT INTO expense_categories(user_id, category_name) VALUES($1, $2)
                           """,
                expense_category.user_id,
                expense_category.category_name,
            )

    async def get_category_by_id(self, category_id: int) -> ExpenseCategory | None:
        async with self.pool.acquire() as conn:
            record = await conn.fetchrow(
                """
                    SELECT * FROM expense_categories WHERE id = $1
                """,
                category_id,
            )
            if record:
                return ExpenseCategory(
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
                DELETE FROM expense_categories WHERE id = $1
            """,
                category_id,
            )

    async def get_categories_by_user(self, user: User) -> list[ExpenseCategory]:
        async with self.pool.acquire() as conn:
            records = await conn.fetch(
                """
                SELECT * FROM expense_categories WHERE user_id = $1
            """,
                user.id,
            )
            categories = []
            for record in records:
                category = ExpenseCategory(
                    id=record["id"],
                    user_id=record["user_id"],
                    category_name=record["category_name"],
                )
                categories.append(category)
            return categories
