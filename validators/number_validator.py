"""Декоратор для валидации входящего значения Income"""

import asyncio
from typing import Awaitable


def is_number(argument: str):
    """Метод проверяет, что входное значение является int или float числом"""
    try:
        _ = float(argument)
        return True
    except ValueError:
        return False


def isOverflow(num, width=32):
    """Проверка на переполнение типа"""
    try:
        num = int(num)
        if num > 0 and num > 2 ** (width - 1) - 1:
            return True
        elif num < 0 and abs(num) > 2 ** (width - 1):
            return True
        return False
    except Exception:
        return True


def validate_number(coroutine_func: Awaitable):
    """Декоратор для асинхронной функции.
    Используется для валидации того, что входной аргумент = число"""

    async def wrapper(*args, **kwargs):
        """Асинхронная свертка для корутины"""

        is_kwargs = not kwargs
        is_str = not isinstance(kwargs["upd"].text, str)
        main_check = not is_number(kwargs["upd"].text)
        is_large_number = isOverflow(kwargs["upd"].text)
        if is_kwargs or is_str or main_check:
            raise ValueError("Значение должно быть формата 12345")
        if is_large_number:
            raise ValueError("Вы слишком богаты, информация ушла в ФСБ")
        task = asyncio.create_task(coroutine_func(*args, **kwargs))
        result = await task

        return result

    return wrapper
