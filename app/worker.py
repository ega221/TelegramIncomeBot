"""Pylint просит докстринг к импортам"""
import asyncio
from typing import List
from client.client import TgClient


async def delay(delay_seconds: int, message: str) -> int:
    print(f'засыпаю на {delay_seconds} сек с сообщения {message}')
    await asyncio.sleep(delay_seconds)
    print(f'сон в течение {delay_seconds} сек с сообщения {message} закончился')
    return delay_seconds


class Worker:
    """Обработка задач из очереди"""
    def __init__(self, token: str, queue: asyncio.Queue, concurrent_workers: int):
        self.tg_client = TgClient(token)
        self.queue = queue
        self.concurrent_workers = concurrent_workers
        self._tasks: List[asyncio.Task] = []

    async def handle_update(self, upd):
        """Неприрывное считывание сообщений из бобота"""
        # print(upd)
        await delay(10, upd['message']['text'])
        # await asyncio.create_task(delay(3, upd['message']['text']))
        # if upd['message']['text'] == '/test':
        #     await self.tg_client.send_message(upd['message']['chat']['id'], 'Привет!\nЯ Бобот.\nЯ научился обрабатывать одну команду!')

    async def _worker(self):
        while True:
            upd = await self.queue.get()
            try:
                await self.handle_update(upd)
            finally:
                self.queue.task_done()

    async def start(self):
        """Запуск добавления задач в очереди"""
        self._tasks = [asyncio.create_task(self._worker()) for _ in range(self.concurrent_workers)]

    async def stop(self):
        """Остановка бота"""
        # try:
        #     await asyncio.wait_for(self.queue.join(), timeout=60)
        # finally:
        await self.queue.join()
        for t in self._tasks:
            t.cancel()
