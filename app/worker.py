"""Pylint просит докстринг к импортам"""

import asyncio

from client.client import TgClient
from dispatcher.dispatcher import Dispatcher
from model.tg_update import Update


async def delay(delay_seconds: int, message: str) -> int:
    print(f"засыпаю на {delay_seconds} сек с сообщения {message}")
    await asyncio.sleep(delay_seconds)
    print(f"сон в течение {delay_seconds} сек с сообщения {message} закончился")
    return delay_seconds


class Worker:
    """Обработка задач из очереди"""

    def __init__(
        self,
        queue: asyncio.Queue,
        tg_client: TgClient,
        dispatcher: Dispatcher,
        queue_timeout: int = 60,
    ):
        self.queue_timeout = queue_timeout
        self.tg_client = tg_client
        self.queue = queue
        self._task: asyncio.Task = None
        self.dispatcher = dispatcher

    async def _do_task(self, upd: Update) -> None:
        """Метод, который передает информацию апдейта в другие серсивы"""
        # task = asyncio.create_task(delay(1, upd.text))
        # await task

        # Отдаем update Диспетчеру
        # task_upd = asyncio.create_task(self.dispatcher.update(upd))
        # res = await task_upd

        res = await asyncio.create_task(self.dispatcher.update(upd))

        # После получения ответа диспетчета отправляем его обратно в чат
        task_send = asyncio.create_task(
            self.tg_client.send_message(res.telegram_id, res.text)
        )
        await task_send
        self.queue.task_done()

    async def _worker(self):
        """Работяга, который достает апдейты из очереди и запускает асинхронную задачу"""
        while True:
            upd = await self.queue.get()
            asyncio.create_task(self._do_task(upd))

    async def start(self):
        """Запуск воркера"""
        self._task = asyncio.create_task(self._worker())

    async def stop(self):
        """Метод, который останавливает воркер и прекращает задачу"""
        await asyncio.gather(self.queue.join())
        self._task.cancel()
