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

        is_kwargs = not kwargs
        is_str = not isinstance(kwargs["upd"].text, str)
        main_check = not is_string_with_letters(kwargs["upd"].text)
        if is_kwargs or is_str or main_check:
            raise ValueError("Категория должна быть строкой, содержащей только буквы")
        task = asyncio.create_task(coroutine_func(*args, **kwargs))
        result = await task

        return result

    return wrapper
