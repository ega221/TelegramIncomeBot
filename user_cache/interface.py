from model.transient_income import TransientIncome
from model.transient_expense import TransientExpense


class UserCache:
    def drop(self, telegram_id: int) -> None:
        pass

    def update(self, telegram_id: int, payload: TransientIncome | TransientExpense) -> None:
        pass

    def get(self, telegram_id: int) -> TransientIncome | TransientExpense:
        pass
