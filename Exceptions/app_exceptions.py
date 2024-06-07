"""Модуль с ошибками"""


class BaseAppException(Exception):
    """Базовоя ошибка"""
    def __init__(self, msg: str = ""):
        self.msg = msg
        super().__init__(self.msg)


class TransactionException(BaseAppException):
    """Ошибка транзакции"""
    pass
