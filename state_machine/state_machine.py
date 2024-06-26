"""Модуль с машиной состояний"""

from config.state_list import StateEnum
from services.interface import Service, UserService


class StateMachine:
    """Машина состояний пользователей"""

    def __init__(
        self,
        income_service: Service,
        expense_service: Service,
        user_service: UserService,
        state_enum: StateEnum,
    ):
        # Ключ - telegram_id, значение state
        self.hash_map = {}
        self.income_service = income_service
        self.expense_service = expense_service
        self.user_service = user_service
        self.state_enum = state_enum

    def set_status(self, telegram_id: str):
        """Установка статуса пользователя"""
        self.hash_map[telegram_id] = self.state_enum.idle

    def get_status(self, telegram_id: str) -> StateEnum:
        """Получение статуса пользователя"""

        return self.hash_map.get(telegram_id, self.state_enum.idle)

    def set_next_status(self, telegram_id: str):
        """Установка следующего статуса"""
        current_state = self.hash_map.get(telegram_id)
        print(current_state)
        self.hash_map[telegram_id] = current_state.nxt

    def get_func(self, telegram_id: str) -> callable:
        """Получение функции, которую необходимо вызвать"""
        return self.hash_map.get(telegram_id).func

    def set_make_income(self, telegram_id: str):
        """Установление статуса для /make_income"""
        self.hash_map[telegram_id] = self.state_enum.init_income

    def set_make_expense(self, telegram_id: str):
        """Установление статуса для /make_expense"""
        self.hash_map[telegram_id] = self.state_enum.init_expense

    def set_choosing(self, telegram_id: str):
        """Установление статуса 'выбора команды'"""
        self.hash_map[telegram_id] = self.state_enum.choosing
