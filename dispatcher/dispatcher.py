# """Модуль с реализацией диспетчера"""

# import asyncio

# from config.command_list import CommandsEnum
# from config.status_list import StatusEnum
# from model.response_templates import Update


# class Dispatcher:
#     """Класс - диспетчер, который принимает update из tg,
#     спрашивает у state машины где находится конкретный пользователь
#     и вызывает нужный серсив
#     """

#     def __init__(self) -> None:
#         # TODO: Добавить машину
#         self.state_machine = None

#     async def update(self, upd):
#         """Метод, который обращается к state machine
#         и перенаправляет update в соответствующий сервис
#         """
#         # state = self.state_machine.get_status(upd["chat_id"])
#         result = upd

#         # try:
#         #     # Если статус = начальный и сообщение является командой
#         #     if (state.status == StatusEnum.idle) and (
#         #         upd.message in Commands.get_commands()
#         #     ):
#         #         # Вызывается метод, инициализирующий нужный по команде сервис
#         #         if upd.message == Commands.cansel:
#         #             # TODO: Возвращаем все состояние
#         #             pass
#         #         elif upd.message == Commands.start:
#         #             # TODO: Вызвать метод "start"
#         #             pass
#         #         else:
#         #             # Иначе инициализируется работа сервиса
#         #             service = self.get_service_by_command(upd.message)
#         #             task = asyncio.create_task(service.initiate(upd["chat_id"]))
#         #             result = await task
#         #     else:
#         #         # Иначе вызывается просто продолжения методов из сервисов
#         #         task = asyncio.create_task(self.to_service(state, upd))
#         #         result = await task
#         # except Exception as e:
#         #     result = e

#         return Update(chat_id=upd.chat_id, text=result.text, update_id=upd.update_id)

#     @staticmethod
#     async def to_service(state, upd):
#         """Отправка update в нужный сервис"""
#         task = asyncio.create_task(state.func(upd))
#         result = await task

#         return result

#     # @staticmethod
#     # async def get_service_by_command(command: str):
#     #     """Возвращает сервис, который необходимо инициализировать"""
#     #     income_list = [CommandsEnum.make_income, CommandsEnum.get_income_categories]
#     #     expense_list = [CommandsEnum.make_expense, CommandsEnum.get_expense_categories]

#     #     # service = None
#     #     # if command in income_list:
#     #     #     service = IncomeService
#     #     # elif command in expense_list:
#     #     #     service = ExpenseService

#     #     return service
