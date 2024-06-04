"""Модуль с реализацией диспетчера"""

import asyncio


class Dispatcher:
    """Класс - диспетчер, который принимает update из tg,
    спрашивает у state машины где находится конкретный пользователь
    и вызывает нужный серсив
    """

    def __init__(self) -> None:
        self.state_machine = None

    async def update(self, upd):
        """Метод, который обращается к state machine
        и перенаправляет update в соответствующий сервис
        """
        state = self.state_machine.get_status(upd["chat_id"])

        # Если статус = начальный и сообщение является командой
        if (state.status == STATUS.idle) and (upd.message in COMMANDS):
            # Вызывается метод, инициализирующий нужный по команде сервис
            try:
                pass
            except Exception as e:
                result = e
        else:
            # Иначе вызывается просто продолжения методов из сервисов
            try:
                task = asyncio.create_task(self.to_service(state, upd))
                result = await task
            except Exception as e:
                result = e

        return result

    async def to_service(self, state, upd):
        """Отправка update в нужный сервис"""
        task = asyncio.create_task(state.func(upd))
        result = await task

        return result
