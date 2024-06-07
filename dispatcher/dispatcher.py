# """Модуль с реализацией диспетчера"""

import asyncio

from config.command_list import CommandsEnum
from config.status_list import StatusEnum
from model.tg_update import Update
from services.expense_service.expense_service_impl import ExpenseServiceImpl
from services.income_service.income_service_impl import IncomeServiceImpl
from services.interface import Service
from user_cache.interface import UserCache


class Dispatcher:
    """Класс - диспетчер, который принимает update из tg,
    спрашивает у state машины где находится конкретный пользователь
    и вызывает нужный серсив
    """

    def __init__(
        self,
        income_service: IncomeServiceImpl,
        expense_service: ExpenseServiceImpl,
        user_cache: UserCache,
    ) -> None:
        self.state_machine = None
        self.income_service = income_service
        self.expense_service = expense_service
        self.user_cache = user_cache

    async def update(self, upd: Update) -> Update:
        """Метод, который обращается к state machine
        и перенаправляет update в соответствующий сервис
        """
        state = self.state_machine.get_status(upd.telegram_id)
        result = Update(telegram_id=upd.telegram_id, text="", update_id=upd.update_id)

        try:
            # Если статус = начальный и сообщение является командой
            if (state.status == StatusEnum.idle) and (
                upd.text in CommandsEnum.get_commands()
            ):
                # Вызывается метод, инициализирующий нужный по команде сервис
                if upd.text == CommandsEnum.cancel:
                    # TODO: Добавить ссылку на начальное сообщение
                    self.user_cache.drop(upd.telegram_id)
                    message = "СООБЩЕНИЕ НАЧАЛЬНОЕ"
                elif upd.message == CommandsEnum.start:
                    # TODO: Вызвать метод "save" из UserService
                    message = "СООБЩЕНИЕ НАЧАЛЬНОЕ"
                    pass
                else:
                    # Иначе инициализируется работа сервиса
                    service = self.get_service_by_command(upd.text)
                    task = asyncio.create_task(service.initiate(upd.telegram_id))
                    message = await task
            else:
                # Иначе вызывается просто продолжения методов из сервисов
                task = asyncio.create_task(state.func(upd))
                message = await task
        except Exception:
            # TODO: Отлавливать какие-то конкретные исключения
            pass
        result.text = message
        return result

    async def get_service_by_command(self, command: str) -> Service:
        """Возвращает сервис, который необходимо инициализировать"""
        income_list = [CommandsEnum.make_income]
        expense_list = [CommandsEnum.make_expense]

        service = None
        if command in income_list:
            service = self.income_service
        elif command in expense_list:
            service = self.expense_service
        else:
            raise KeyError("Команда неизвестная")
        return service
