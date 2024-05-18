import asyncpg

from model.user import User
from repository.interface import UserRepository


class UserRepositoryImpl(UserRepository):
    def __init__(self, pool: asyncpg.pool.Pool):
        self.pool = pool

    async def save(self, user: User):
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
             INSERT INTO users(id) VALUES($1)
            """,
                user.id,
            )

    async def get_user_by_id(self, user_id) -> User | None:
        async with self.pool.acquire() as conn:
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

    async def delete_user_by_id(self, user_id):
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                            DELETE FROM users WHERE id = $1
                        """,
                user_id,
            )
