"""Pylint просит докстринг к импортам"""

import asyncio
from typing import Optional

import aiohttp

from model.tg_update import Update


class TgClient:
    """Клиент для общения с Telegram API"""

    def __init__(
        self, token: str = "", tg_api_url: str = "https://api.telegram.org/bot"
    ) -> None:
        self.token = token
        self.tg_api_url = tg_api_url

    def get_url(self, method: str) -> str:
        """Запрос к Telegram API"""
        return f"{self.tg_api_url}{self.token}/{method}"

    async def get_updates(
        self, offset: Optional[int] = None, timeout: int = 0
    ) -> Update:
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

        res_dict = res_dict["result"][0]

        return Update(
            telegram_id=res_dict["message"]["chat"]["id"],
            text=res_dict["message"]["text"],
            update_id=res_dict["update_id"],
        )

    async def get_updates_in_objects(
        self, offset: Optional[int] = None, timeout: int = 0
    ) -> Update:
        """Получение сообщений"""
        task = asyncio.create_task(self.get_updates(offset=offset, timeout=timeout))
        res_dict = await task
        return res_dict

    async def send_message(self, chat_id: int, text: str) -> None:
        """Отправка сообщений через бота"""
        url = self.get_url("sendMessage")
        payload = {"chat_id": chat_id, "text": text}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as resp:
                task = asyncio.create_task(resp.json())
                await task
