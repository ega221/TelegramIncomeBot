"""Pylint просит докстринг к импортам"""

import asyncio
from typing import Optional
import aiohttp


class TgClient:
    """Клиент для общения с Telegram API"""

    def __init__(
        self, token: str = "", tg_api_url: str = "https://api.telegram.org/bot"
    ):
        self.token = token
        self.tg_api_url = tg_api_url

    def get_url(self, method: str):
        """Запрос к Telegram API"""
        return f"{self.tg_api_url}{self.token}/{method}"

    async def get_me(self) -> dict:
        """Вывод информации о боботе"""
        url = self.get_url("getMe")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                task = asyncio.create_task(resp.json())
                res_dict = await task
                return res_dict

    async def get_updates(self, offset: Optional[int] = None, timeout: int = 0) -> dict:
        """Получение сообщений с бота"""
        url = self.get_url("getUpdates")
        params = {}
        if offset:
            params["offset"] = offset
        if timeout:
            params["timeout"] = timeout
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as resp:
                task = asyncio.create_task(resp.json())
                res_dict = await task
                return res_dict

    async def get_updates_in_objects(
        self, offset: Optional[int] = None, timeout: int = 0
    ):
        """Получение сообщений"""
        res_dict = await asyncio.create_task(
            self.get_updates(offset=offset, timeout=timeout)
        )
        return res_dict

    async def send_message(self, chat_id: int, text: str):
        """Отправка сообщений через бота"""
        url = self.get_url("sendMessage")
        payload = {"chat_id": chat_id, "text": text}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as resp:
                task = asyncio.create_task(resp.json())
                res_dict = await task
                return res_dict
