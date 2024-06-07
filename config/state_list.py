"""Файл, содержащий enum со всеми командами"""

from enum import Enum

from services.interface import Service, UserService


class StateEnum:
    """str enum, который хранит в себе все команды"""

    def __init__(self,
                 income_service: Service,
                 expense_service: Service,
                 user_service: UserService):
        self.income_service = income_service
        self.expense_service = expense_service
        self.user_service = user_service

        setting_expense_value = Inner("SETTING_EXPENSE_VALUE", None)
        setting_expense_date = Inner("SETTING_EXPENSE_DATE", setting_expense_value, None)
        setting_expense_category = Inner("SETTING_EXPENSE_CATEGORY", setting_expense_date, None)
        setting_income_value = Inner("SETTING_INCOME_VALUE", None, None)
        setting_income_date = Inner("SETTING_INCOME_DATE", setting_income_value, None)
        setting_income_category = Inner("SETTING_INCOME_CATEGORY", setting_income_date, None)
        idle = Inner("IDLE", None, None)

    class Inner:
        def __init__(self, value, nxt, func):
            self.value = value
            self.nxt = nxt
            self.func = func

    """
    idle = "IDLE"
    setting_income_category = "SETTING_INCOME_CATEGORY"
    setting_income_date = "SETTING_INCOME_DATE"
    setting_income_value = "SETTING_INCOME_VALUE"
    setting_expense_category = "SETTING_EXPENSE_CATEGORY"
    setting_expense_date = "SETTING_EXPENSE_DATE"
    setting_expense_value = "SETTING_EXPENSE_VALUE"
    """

    @classmethod
    def get_status(cls):
        """Метод возвращает список из всех доступных команд"""
        return [value.value for value in cls]
