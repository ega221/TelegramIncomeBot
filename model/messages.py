from enum import Enum


class Message(Enum):
    GREETING = "Доброго времени суток это бот"
    INITIATE_INCOME = "Выберите категорию доходов"
    INITIATE_EXPENSE = "Выберите категорию расходов"
    DATE_SET = "Дата установлена"
    CATEGORY_SET = "Категория установлена"
    VALUE_SET = "Значение установлено"
    INCOME_SAVED = "Доход сохранен"
    INCOME_DROPPED = "Доход сброшен"
    EXPENSE_SAVED = "Расход сохранен"
    EXPENSE_DROPPED = "Расход сброшен"
    CANCEL = "Команда отменена"
    UNKNOWN_COMMAND = "Неизвестная команда"
