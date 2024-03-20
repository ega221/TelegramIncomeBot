"""Pylint просит докстринг к импортам"""

import asyncio
from client.client import TgClient

async def delay(delay_seconds: int, message: str) -> int:
    print(f"засыпаю на {delay_seconds} сек с сообщения {message}")
    await asyncio.sleep(delay_seconds)
    print(f"сон в течение {delay_seconds} сек с сообщения {message} закончился")
    return delay_seconds


class Worker:
    """Обработка задач из очереди"""

    def __init__(self, queue: asyncio.Queue, tg_client: TgClient):
        self.tg_client = tg_client
        self.queue = queue
        self._task: asyncio.Task = None

    async def _do_task(self, upd):
        """Метод, который передает информацию апдейта в другие серсивы"""
        try:
            task = asyncio.create_task(delay(3, upd["message"]["text"]))
            await task
            # if upd['message']['text'] == '/test':
            # await self.tg_client.send_message(upd['message']['chat']['id'], 'Привет!\nЯ Бобот.\nЯ научился обрабатывать одну команду!')
        finally:
            self.queue.task_done()

    async def _worker(self):
        """Работяга, который достает апдейты из очереди и запускает асинхронную задачу"""
        while True:
            task_get_upd = self.queue.get()
            upd = await task_get_upd
            asyncio.create_task(self._do_task(upd))

    async def start(self):
        """Запуск воркера"""
        self._task = asyncio.create_task(self._worker())

    async def stop(self):
        """Метод, который останавливает воркер и прекращает задачу"""
        try:
            await asyncio.wait_for(self.queue.join(), timeout=60)
        finally:
            self._task.cancel()
