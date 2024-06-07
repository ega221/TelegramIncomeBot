"""Pylint просит докстринг к импортам"""

import asyncio
import datetime
import os

import asyncpg
import nest_asyncio
from dotenv import load_dotenv

from app.bot import Bot
from dispatcher.dispatcher import Dispatcher

nest_asyncio.apply()
load_dotenv()


async def create_pool():
    return await asyncpg.create_pool(
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        port=os.getenv("PG_PORT"),
        host=os.getenv("PG_HOST"),
    )


async def run():
    """Метод для запуска бота."""
    loop = asyncio.get_event_loop()
    bot = Bot(
        token=os.getenv("API_TOKEN"),
        queue_maxsize=int(os.getenv("QUEUE_MAX_SIZE")),
        queue_timeout=int(os.getenv("QUEUE_TIMEOUT")),
        update_timeout=int(os.getenv("UPDATES_TIMEOUT")),
        tg_api_url=os.getenv("TG_URL"),
        dispetcher=Dispatcher(
            income_service=None, expense_service=None, user_cache=None
        ),
    )

    try:
        print("bot has been started")
        await loop.create_task(bot.start())
        loop.run_forever()
    except KeyboardInterrupt:
        print("\nstopping", datetime.datetime.now())
        loop.run_until_complete(bot.stop())
        print("bot has been stopped", datetime.datetime.now())


if __name__ == "__main__":
    asyncio.run(run())
