# """Модуль с реализацией диспетчера"""

import asyncio

from config.command_list import CommandsEnum
from config.status_list import StatusEnum
from model.messages import Message
from model.tg_update import Update
from services.expense_service.expense_service_impl import ExpenseServiceImpl
from services.income_service.income_service_impl import IncomeServiceImpl
from services.interface import Service
from services.user_service.user_service_impl import UserServiceImpl
from user_cache.cache.user_cache_impl import UserCacheImpl


class Dispatcher:
    """Класс - диспетчер, который принимает update из tg,
    спрашивает у state машины где находится конкретный пользователь
    и вызывает нужный серсив
    """

    def __init__(
        self,
        income_service: IncomeServiceImpl,
        expense_service: ExpenseServiceImpl,
        user_cache: UserCacheImpl,
        user_service: UserServiceImpl,
    ) -> None:
        self.state_machine = None
        self.income_service = income_service
        self.expense_service = expense_service
        self.user_service = user_service
        self.user_cache = user_cache

    async def update(self, upd: Update) -> Update:
        """Метод, который обращается к state machine
        и перенаправляет update в соответствующий сервис
        """
        state = self.state_machine.get_status(upd.telegram_id)
        result = Update(telegram_id=upd.telegram_id, text="", update_id=upd.update_id)
        message = Message.UNKNOWN_COMMAND
        try:
            # Если статус = начальный и сообщение является командой /start
            if (state.status == StatusEnum.idle) and (
                upd.message == CommandsEnum.start
            ):
                self.user_service.save(upd)
                message = Message.GREETING
            # Если статус = начальный и сообщение является командой /start
            else:
                if upd.text in [CommandsEnum.make_income]:
                    task = asyncio.create_task(self.income_service.initiate(upd))
                    message = await task
                elif upd.text in [CommandsEnum.make_expense]:
                    task = asyncio.create_task(self.expense_service.initiate(upd))
                    message = await task
                elif upd.text == CommandsEnum.cancel:
                    self.user_cache.drop(upd.telegram_id)
                    message = Message.CANCEL
                    # TODO: Сказать стейт машине что этот пользователь = начальное состояние
                else:
                    task = asyncio.create_task(state.func(upd))
                    message = await task
        except Exception:
            # TODO: Отлавливать какие-то конкретные исключения
            pass
        result.text = message
        return result
