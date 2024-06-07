"""Декоратор для валидации входящей категории"""

import asyncio
from typing import Awaitable


def is_string_with_letters(argument: str):
    """Метод проверяет, что входящий аргумент является строкой"""
    return isinstance(argument, str) and argument.isalpha()


def validate_category(coroutine_func: Awaitable):
    """Декоратор для валидации строки с категорией.
    Он проверяет, что в строке содержатся только буквы"""

    async def wrapper(*args, **kwargs):
        """Асинхронная свертка для корутины"""
        if (
            not kwargs
            or not isinstance(kwargs["upd"], str)
            or not is_string_with_letters(kwargs["upd"].text)
        ):
            raise ValueError("Категория должна быть строкой, содержащей только буквы")
        task = asyncio.create_task(coroutine_func(*args, **kwargs))
        result = await task

        return result

    return wrapper
