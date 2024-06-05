"""Модуль, реализующий интерфейс сервиса"""

from datetime import datetime
from model.transient_expense import TransientExpense
from model.transient_income import TransientIncome


class Service:
    async def initiate(self, telegram_id: int) -> TransientIncome | TransientExpense:
        pass

    async def set_category(self, telegram_id: int, category_id: int) -> TransientIncome | TransientExpense:
        pass

    async def set_date(self, telegram_id: int, date: datetime) -> TransientIncome | TransientExpense:
        pass

    async def set_value(self, telegram_id: int, value: int) -> TransientIncome | TransientExpense:
        pass

    async def save(self, telegram_id: int) -> TransientIncome | TransientExpense:
        pass

    async def drop(self, telegram_id: int) -> None:
        pass
