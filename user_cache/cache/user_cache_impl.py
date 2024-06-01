from model.income import Income
from model.expense import Expense
from user_cache.interface import UserCache


class UserCacheImpl(UserCache):
    def __init__(self):
        self.hash_map = {}

    def drop(self, index: int) -> None:
        self.hash_map.pop(index)

    def update(self, user_id: int, payload: Income | Expense) -> None:
        self.hash_map[user_id] = payload

    def get(self, user_id: int) -> Income | Expense:
        return self.hash_map.get(user_id)
