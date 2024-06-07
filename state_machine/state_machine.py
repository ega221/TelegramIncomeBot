from config.state_list import StateEnum
from services.interface import Service, UserService


class StateMachine:
    def __init__(self,
                 income_service: Service,
                 expense_service: Service,
                 user_service: UserService):
        # Ключ - telegram_id, значение state
        self.hash_map = {}
        self.income_service = income_service
        self.expense_service = expense_service
        self.user_service = user_service

    async def get_status(self, telegram_id: str) -> StateEnum:
        return self.hash_map.get(telegram_id, StateEnum.idle)

    async def set_next_status(self, telegram_id: str):
        current_state = self.hash_map.get(telegram_id)
        self.hash_map[telegram_id] = current_state.nxt

    async def get_func(self, telegram_id: str) -> callable:
        return self.hash_map.get(telegram_id).func
