"""Декоратор для валидации входящей даты"""

import asyncio
from datetime import datetime
from typing import Awaitable


def is_date_string(argument: str):
    """Метод проверяет, что дата написана в формате DD-MM-YYYY"""
    try:
        datetime.strptime(argument, "%d-%m-%Y")
        return True
    except ValueError:
        return False


def validate_date(coroutine_func: Awaitable):
    """Декоратор для валидации даты.
    Он проверяет, что дата написана в формате DD-MM-YYYY"""

    async def wrapper(*args, **kwargs):
        """Асинхронная свертка для корутины"""
        if (
            not kwargs
            or not isinstance(kwargs["upd"], str)
            or not is_date_string(kwargs["upd"].text)
        ):
            raise ValueError("Дата должна быть строкой в формате DD-MM-YYYY")
        task = asyncio.create_task(coroutine_func(*args, **kwargs))
        result = await task

        return result

    return wrapper
