"""Pylint просит докстринг к импортам"""
import asyncio
from app.poller import Poller
from app.worker import Worker


class Bot:
    """Класс для запуска и остановки бота."""
    def __init__(self, token: str, n: int):
        self.queue = asyncio.Queue()
        self.poller = Poller(token, self.queue)
        self.worker = Worker(token, self.queue, n)

    async def start(self):
        """Класс для запуска работы бота."""
        await self.poller.start()
        await self.worker.start()

    async def stop(self):
        """Класс для остановки работы бота."""
        await self.poller.stop()
        await self.worker.stop()
