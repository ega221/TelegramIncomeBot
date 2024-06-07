"""Pylint просит докстринг к импортам"""

import asyncio

from app.poller import Poller
from app.worker import Worker
from client.client import TgClient
from dispatcher.dispatcher import Dispatcher


class Bot:
    """Класс для запуска и остановки бота."""

    def __init__(
        self,
        token: str,
        queue_maxsize: int,
        queue_timeout: int,
        update_timeout: int,
        tg_api_url: str,
        dispetcher: Dispatcher
    ):
        self.tg_client = TgClient(token, tg_api_url)
        self.queue = asyncio.Queue(maxsize=queue_maxsize)
        self.poller = Poller(self.queue, self.tg_client, update_timeout=update_timeout)
        self.worker = Worker(
            self.queue,
            self.tg_client,
            queue_timeout=queue_timeout,
            dispatcher=dispetcher,
        )

    async def start(self):
        """Метод для запуска работы бота."""
        await self.poller.start()
        await self.worker.start()

    async def stop(self):
        """Метод для остановки работы бота."""
        await self.poller.stop()
        await self.worker.stop()
