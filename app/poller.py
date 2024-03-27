"""Pylint просит докстринг к импортам"""

import asyncio
from client.client import TgClient


class Poller:
    """Получение апдейтов из телеграма и добавление их в очередь"""

    def __init__(self, queue: asyncio.Queue, tg_client: TgClient, update_timeout: int):
        self.tg_client = tg_client
        self.queue = queue
        self.update_timeout = update_timeout
        self._task: asyncio.Task = None
        

    async def _worker(self):
        """Работяга, который выполняет получение апдейтов из телеграма и добавлением их в очередь"""
        offset = 0
        while True:
            task = asyncio.create_task(
                self.tg_client.get_updates_in_objects(offset=offset, timeout=self.update_timeout)
            )
            res = await task
            for upd in res["result"]:
                offset = upd["update_id"] + 1
                await self.queue.put(upd)

    async def start(self):
        """Метод, который запускает поллер"""
        self._task = asyncio.create_task(self._worker())

    async def stop(self):
        """Метод, который останавливает поллер и прекращает задачу"""
        self._task.cancel()
