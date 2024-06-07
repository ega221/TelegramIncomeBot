# """Модуль с реализацией диспетчера"""

import asyncio
import sys
import traceback

from Exceptions.app_exceptions import BaseAppException
from config.command_list import CommandsEnum
from config.inner import Inner
from config.state_list import StateEnum
from model.messages import Message
from model.tg_update import Update
from services.interface import Service, UserService
from state_machine.state_machine import StateMachine
from user_cache.interface import UserCache


class Dispatcher:
    """Класс - диспетчер, который принимает update из tg,
    спрашивает у state машины где находится конкретный пользователь
    и вызывает нужный серсив
    """

    def __init__(
        self,
        income_service: Service,
        expense_service: Service,
        user_cache: UserCache,
        user_service: UserService,
        state_enum: StateEnum,
        state_machine: StateMachine,
    ) -> None:
        self.state_machine = state_machine
        self.income_service = income_service
        self.expense_service = expense_service
        self.user_service = user_service
        self.user_cache = user_cache
        self.state_enum = state_enum

    async def update(self, upd: Update) -> Update:
        """Метод, который обращается к state machine
        и перенаправляет update в соответствующий сервис
        """
        state: Inner = self.state_machine.get_status(upd.telegram_id)
        result = Update(telegram_id=upd.telegram_id, text="", update_id=upd.update_id)
        message = Message.UNKNOWN_COMMAND
        print("Текущее состояние:", state.value)
        print("update:", upd)
        try:
            # Если статус = начальный и сообщение является командой /start
            if (state.value == self.state_enum.idle.value) and (
                upd.text == CommandsEnum.start
            ):
                await self.user_service.save(upd)
                message = Message.GREETING
                self.state_machine.set_status(upd.telegram_id)
                self.state_machine.set_next_status(upd.telegram_id)
            # Если статус = начальный и сообщение является командой /start
            else:
                if upd.text == CommandsEnum.cancel:
                    print("cancel")
                    self.user_cache.drop(upd.telegram_id)
                    message = Message.CANCEL
                    self.state_machine.set_choosing(upd.telegram_id)
                elif upd.text in [CommandsEnum.make_income]:
                    print("make income")
                    self.state_machine.set_make_income(upd.telegram_id)
                    task = asyncio.create_task(self.income_service.initiate(upd=upd))
                    message = await task
                    self.state_machine.set_next_status(upd.telegram_id)
                elif upd.text in [CommandsEnum.make_expense]:
                    print("make expense")
                    self.state_machine.set_make_expense(upd.telegram_id)
                    task = asyncio.create_task(self.expense_service.initiate(upd=upd))
                    message = await task
                    self.state_machine.set_next_status(upd.telegram_id)
                else:
                    print("other func")
                    if state.func:
                        task = asyncio.create_task(state.func(upd=upd))
                        message = await task
                        self.state_machine.set_next_status(upd.telegram_id)
        except ValueError as e:
            message = str(e)
        except BaseAppException:
            message = "Произошла ошибка :(\nПопробуйте снова"
            self.user_cache.drop(upd.telegram_id)
            self.state_machine.set_choosing(upd.telegram_id)
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            print(e)
        result.text = message
        return result
