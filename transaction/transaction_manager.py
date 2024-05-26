from typing import Protocol
from contextlib import asynccontextmanager


class TransactionManager(Protocol):

    @asynccontextmanager
    async def transaction(self):
        pass

    async def get_connection(self):
        pass
