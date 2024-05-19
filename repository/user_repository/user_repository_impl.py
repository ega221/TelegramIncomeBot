from asyncpg import connection

from model.user import User
from repository.interface import UserRepository


class UserRepositoryImpl(UserRepository):

    async def save(self, conn: connection, user: User):
        await conn.execute(
            """
            INSERT INTO users(id) VALUES($1)
            """,
            user.id,
        )

    async def get_user_by_id(self, conn: connection, user_id) -> User | None:
        record = await conn.fetchrow(
            """
            SELECT * FROM users WHERE id = $1
            """,
            user_id,
        )
        if record:
            return User(id=record["id"])
        else:
            return None

    async def delete_user_by_id(self, conn: connection, user_id):
        await conn.execute(
            """
            DELETE FROM users WHERE id = $1
            """,
            user_id,
        )
