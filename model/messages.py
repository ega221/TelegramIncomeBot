from enum import StrEnum


class Message(StrEnum):
    GREETING = "Доброго времени суток это бот"
    INITIATE_INCOME = "Выберите категорию доходов \nДоступны категории:\n1. Зарплата\n2. Подарки"
    INITIATE_EXPENSE = "Выберите категорию расходов\nДоступны категории:\n1. Продукты\n2. Спортзал"
    DATE_SET = "Дата установлена\nВведите значение дохода:"
    CATEGORY_SET = "Категория установлена. \nВведите дату в формате 'dd-mm-yyyy'"
    VALUE_SET = "Значение установлено."
    INCOME_SAVED = "Доход сохранен"
    INCOME_DROPPED = "Доход сброшен"
    EXPENSE_SAVED = "Расход сохранен"
    EXPENSE_DROPPED = "Расход сброшен"
    CANCEL = "Команда отменена"
    UNKNOWN_COMMAND = "Неизвестная команда"
    ADD_VALUE_MESSAGE = "Если хотите сохранить, то введите любой символ, иначе введите команду /cancel"
