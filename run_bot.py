"""Pylint просит докстринг к импортам"""

import asyncio
import asyncpg
import datetime
import os
import nest_asyncio
from dotenv import load_dotenv
from app.bot import Bot
from repository.expense_category_repository.expense_category_repository_impl import (
    ExpenseCategoryRepositoryImpl,
)
from repository.expense_repository.expense_repository_impl import ExpenseRepositoryImpl
from repository.income_category_repository.income_category_repository_impl import (
    IncomeCategoryRepositoryImpl,
)
from repository.income_repository.income_repository_impl import IncomeRepositoryImpl
from repository.user_repository.user_repository_impl import UserRepositoryImpl

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
    pool = await create_pool()

    user_repository = UserRepositoryImpl(pool)
    expense_category_repository = ExpenseCategoryRepositoryImpl(pool)
    expense_repository = ExpenseRepositoryImpl(pool)
    income_category_repository = IncomeCategoryRepositoryImpl(pool)
    income_repository = IncomeRepositoryImpl(pool)

    bot = Bot(
        token=os.getenv("API_TOKEN"),
        queue_maxsize=int(os.getenv("QUEUE_MAX_SIZE")),
        queue_timeout=int(os.getenv("QUEUE_TIMEOUT")),
        update_timeout=int(os.getenv("UPDATES_TIMEOUT")),
        tg_api_url=os.getenv("TG_URL"),
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
