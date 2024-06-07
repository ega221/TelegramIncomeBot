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


def validate_number(coroutine_func: Awaitable):
    """Декоратор для асинхронной функции.
    Используется для валидации того, что входной аргумент = число"""

    async def wrapper(*args, **kwargs):
        """Асинхронная свертка для корутины"""
        if (
            not kwargs
            or not isinstance(kwargs["upd"].text, str)
            or not is_number(kwargs["upd"].text)
        ):
            raise ValueError("Значение должно быть формата 12345.67 или 12345")
        task = asyncio.create_task(coroutine_func(*args, **kwargs))
        result = await task

        return result

    return wrapper
