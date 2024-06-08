"""Модуль с имплементацией кэша"""

from model.transient_income import TransientIncome
from model.transient_expense import TransientExpense
from user_cache.interface import UserCache


class UserCacheImpl(UserCache):
    """Класс - кэш, который хранит в себе
    промежуточный Income и промежуточный Expense
    """

    def __init__(self):
        self.hash_map = {}

    def drop(self, telegram_id: int) -> None:
        """Метод, который удаляет из кэша запись
        о пользователе с соответствующим telegram_id
        """
        if (self.hash_map.get(telegram_id, None)):
            self.hash_map.pop(telegram_id)

    def update(self, telegram_id: int, payload: TransientIncome | TransientExpense) -> None:
        """Метод обновляет запись в кэш по-соответствующему telegram_id
        и добавляет ее, если записи с таким id еще не существует
        """
        self.hash_map[telegram_id] = payload

    def get(self, telegram_id: int) -> TransientIncome | TransientExpense:
        """Метод возвращает запись с временным TransientIncome
        или TransientExpense
        """
        return self.hash_map.get(telegram_id)
