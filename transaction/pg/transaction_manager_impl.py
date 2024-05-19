from Exceptions.app_exceptions import TransactionException, BaseAppException
from transaction.transaction_manager import TransactionManager
from contextlib import asynccontextmanager
from asyncpg import connection, pool, transaction
from typing import Iterator


class TransactionManagerImpl(TransactionManager):
    def __init__(self, connection_pool: pool):
        self._connection_pool = connection_pool

    @asynccontextmanager
    async def transaction(self) -> Iterator[transaction]:
        async with self._connection_pool.acquire() as conn:
            async with conn.transaction():
                try:
                    yield conn
                except Exception as e:
                    raise TransactionException(e)

    @asynccontextmanager
    async def get_connection(self) -> connection:
        async with self._connection_pool.acquire() as conn:
            async with conn.transaction():
                try:
                    print("Транзакция началась")
                    yield conn
                except Exception as e:
                    raise BaseAppException(e)
