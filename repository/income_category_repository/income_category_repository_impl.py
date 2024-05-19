from asyncpg import connection

from model.income_category import IncomeCategory
from model.user import User

from repository.interface import IncomeCategoryRepository


class IncomeCategoryRepositoryImpl(IncomeCategoryRepository):
    async def save(self, conn: connection, income_category: IncomeCategory):
        result = await conn.fetchrow(
            """
            INSERT INTO income_categories(user_id, category_name) VALUES($1, $2) RETURNING id
            """,
            income_category.user_id,
            income_category.category_name,
        )
        income_category.id = result["id"]
        return income_category

    async def get_category_by_id(self, conn: connection, category_id: int) -> IncomeCategory | None:
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

    async def delete_category_by_id(self, conn: connection, category_id: int):
        await conn.execute(
            """
            DELETE FROM income_categories WHERE id = $1
            """,
            category_id,
        )

    async def get_categories_by_user(self, conn: connection, user: User) -> list[IncomeCategory]:
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
