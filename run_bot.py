"""Pylint просит докстринг к импортам"""

import asyncio
import datetime
import os
import nest_asyncio
from dotenv import load_dotenv
from app.bot import Bot

nest_asyncio.apply()
load_dotenv()


async def run():
    """Метод для запуска бота."""
    loop = asyncio.get_event_loop()

    bot = Bot(
        token=os.getenv("API_TOKEN"),
        queue_maxsize=int(os.getenv("QUEUE_MAX_SIZE")),
        queue_timeout=int(os.getenv("QUEUE_TIMEOUT")),
        update_timeout=int(os.getenv("UPDATES_TIMEOUT")),
        tg_api_url=os.getenv('TG_URL')
        )

    try:
        print("bot has been started")
        loop.create_task(bot.start())
        loop.run_forever()
    except KeyboardInterrupt:
        print("\nstopping", datetime.datetime.now())
        loop.run_until_complete(bot.stop())
        print("bot has been stopped", datetime.datetime.now())


if __name__ == "__main__":
    asyncio.run(run())
