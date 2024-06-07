"""Файл, содержащий enum со всеми командами"""

from enum import Enum

from config.inner import Inner
from services.interface import Service, UserService


class StateEnum:
    """str enum, который хранит в себе все команды"""

    def __init__(self,
                 income_service: Service,
                 expense_service: Service,
                 user_service: UserService,
                 Inner_object: Inner):
        
        self.income_service = income_service
        self.expense_service = expense_service
        self.user_service = user_service
        self.Inner_object = Inner_object
        
        # CHOOSING (он изменяется динамически)
        self.choosing = self.Inner_object("CHOOSING", None, None)

        # EXPENSE
        self.save_expense = self.Inner_object("SAVING_EXPENSE", self.choosing, self.expense_service.save)
        self.setting_expense_value = self.Inner_object("SETTING_EXPENSE_VALUE", self.save_expense, self.expense_service.set_value)
        self.setting_expense_date = self.Inner_object("SETTING_EXPENSE_DATE", self.setting_expense_value, self.expense_service.set_date)
        self.setting_expense_category = self.Inner_object("SETTING_EXPENSE_CATEGORY", self.setting_expense_date, self.expense_service.set_category)
        self.init_expense = self.Inner_object("INIT_EXPENSE", self.setting_expense_category, self.expense_service.initiate)

        # INCOME
        self.save_income = self.Inner_object("SAVING_INCOME", self.choosing, self.income_service.save)
        self.setting_income_value = self.Inner_object("SETTING_INCOME_VALUE", self.save_income, self.income_service.set_value)
        self.setting_income_date = self.Inner_object("SETTING_INCOME_DATE", self.setting_income_value, self.income_service.set_date)
        self.setting_income_category = self.Inner_object("SETTING_INCOME_CATEGORY", self.setting_income_date, self.income_service.set_category)
        self.init_income = self.Inner_object("INIT_INCOME", self.setting_income_category, self.income_service.initiate)

        # IDLE
        self.idle = self.Inner_object("IDLE", self.choosing, None)



    @classmethod
    def get_status(cls):
        """Метод возвращает список из всех доступных команд"""
        return [value.value for value in cls]
