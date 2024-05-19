from asyncpg import connection

from model.expense_category import ExpenseCategory
from model.user import User

from repository.interface import ExpenseCategoryRepository


class ExpenseCategoryRepositoryImpl(ExpenseCategoryRepository):

    async def save(self, conn: connection, expense_category: ExpenseCategory):
        result = await conn.execute(
            """
            INSERT INTO expense_categories(user_id, category_name) VALUES($1, $2) RETURNING id
            """,
            expense_category.user_id,
            expense_category.category_name,
        )
        expense_category.id = result[id]
        return expense_category

    async def get_category_by_id(self, conn: connection, category_id: int) -> ExpenseCategory | None:
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

    async def delete_category_by_id(self, conn: connection, category_id: int):
        await conn.execute(
            """
            DELETE FROM expense_categories WHERE id = $1
            """,
            category_id,
        )

    async def get_categories_by_user(self, conn: connection, user: User) -> list[ExpenseCategory]:
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
