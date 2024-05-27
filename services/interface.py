from datetime import datetime
from model.income import Income
from model.expense import Expense
from typing import Union


class Service:
    async def initiate(self, user_id: int):
        pass

    async def set_category(self, user_id: int, category_id: int) -> Union[Income, Expense]:
        pass

    async def set_date(self, user_id: int, date: datetime) -> Union[Income, Expense]:
        pass

    async def set_value(self, user_id: int, value: int) -> Union[Income, Expense]:
        pass

    async def save(self, user_id: int) -> Union[Income, Expense]:
        pass

    async def drop(self, user_id: int) -> None:
        pass
