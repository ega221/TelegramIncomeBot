"""Pylint просит докстринг к импортам"""
import asyncio
import datetime
import os
from dotenv import load_dotenv
from app.bot import Bot
import nest_asyncio

nest_asyncio.apply()
load_dotenv()



async def run():
    """Метод для запуска бота."""
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    loop = asyncio.get_event_loop()
    bot = Bot(os.getenv("API_TOKEN"), 10)

    try:
        print('bot has been started')
        loop.create_task(bot.start())
        loop.run_forever()
    except KeyboardInterrupt:
        print("\nstopping", datetime.datetime.now())
        loop.run_until_complete(bot.stop())
        print('bot has been stopped', datetime.datetime.now())
    


if __name__ == '__main__':
    asyncio.run(run())
