from datetime import datetime


class IncomeService:
    async def initiate(self, user_id: int):
        pass

    async def set_category(self, user_id: int, category_id: int):
        pass

    async def set_date(self, user_id: int, date: datetime):
        pass

    async def set_value(self, user_id: int, value: int):
        pass

    async def save(self, user_id: int):
        pass

    async def drop(self, user_id: int) -> None:
        pass
