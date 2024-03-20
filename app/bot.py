"""Pylint просит докстринг к импортам"""

import asyncio

from app.poller import Poller
from app.worker import Worker
from client.client import TgClient


class Bot:
    """Класс для запуска и остановки бота."""

    def __init__(self, token: str):
        self.tg_client = TgClient(token)
        self.queue = asyncio.Queue()
        self.poller = Poller(self.queue, self.tg_client)
        self.worker = Worker(self.queue, self.tg_client)

    async def start(self):
        """Метод для запуска работы бота."""
        await self.poller.start()
        await self.worker.start()

    async def stop(self):
        """Метод для остановки работы бота."""
        await self.poller.stop()
        await self.worker.stop()
