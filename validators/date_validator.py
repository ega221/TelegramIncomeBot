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
        is_kwargs = not kwargs
        is_str = not isinstance(kwargs["date"], str)
        main_check = not is_date_string(kwargs["date"])
        if is_kwargs or is_str or main_check:
            raise ValueError("Дата должна быть строкой в формате DD-MM-YYYY")
        task = asyncio.create_task(coroutine_func(*args, **kwargs))
        result = await task

        return result

    return wrapper
