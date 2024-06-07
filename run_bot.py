"""Pylint просит докстринг к импортам"""

import asyncio
import datetime
import os

import asyncpg
import nest_asyncio
from dotenv import load_dotenv

from app.bot import Bot
from config.inner import Inner
from config.state_list import StateEnum
from dispatcher.dispatcher import Dispatcher
from repository.expense_category_repository.expense_category_repository_impl import (
    ExpenseCategoryRepositoryImpl,
)
from repository.expense_repository.expense_repository_impl import ExpenseRepositoryImpl
from repository.income_category_repository.income_category_repository_impl import (
    IncomeCategoryRepositoryImpl,
)
from repository.income_repository.income_repository_impl import IncomeRepositoryImpl
from repository.user_repository.user_repository_impl import UserRepositoryImpl
from services.expense_service.expense_service_impl import ExpenseServiceImpl
from services.income_service.income_service_impl import IncomeServiceImpl
from services.user_service.user_service_impl import UserServiceImpl
from state_machine.state_machine import StateMachine
from transaction.pg.transaction_manager_impl import TransactionManagerImpl
from user_cache.cache.user_cache_impl import UserCacheImpl

nest_asyncio.apply()
load_dotenv()


async def create_pool():
    """Создает poll подключения к БД"""
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
    # Кэш
    cache = UserCacheImpl()

    # Для БД
    connection_pool = await create_pool()
    transaction_manager = TransactionManagerImpl(connection_pool=connection_pool)

    # Все репозитории
    user_repo = UserRepositoryImpl()
    income_repository = IncomeRepositoryImpl()
    expense_repository = ExpenseRepositoryImpl()
    income_category_repository = IncomeCategoryRepositoryImpl()
    expense_category_repository = ExpenseCategoryRepositoryImpl()

    # Сервисы
    income_service = IncomeServiceImpl(
        user_cache=cache,
        transaction_manager=transaction_manager,
        user_repo=user_repo,
        income_cat_repo=income_category_repository,
        income_repo=income_repository,
    )
    expense_service = ExpenseServiceImpl(
        user_cache=cache,
        transaction_manager=transaction_manager,
        user_repo=user_repo,
        expense_cat_repo=expense_category_repository,
        expense_repo=expense_repository,
    )
    user_service = UserServiceImpl(
        transaction_manager=transaction_manager,
        user_repo=user_repo,
    )
    state_enum = StateEnum(
        income_service=income_service,
        expense_service=expense_service,
        user_service=user_service,
        inner_object=Inner,
    )
    state_machine = StateMachine(
        income_service=income_service,
        expense_service=expense_service,
        user_service=user_service,
        state_enum=state_enum,
    )
    dispatcher = Dispatcher(
        income_service=income_service,
        expense_service=expense_service,
        user_service=user_service,
        user_cache=cache,
        state_enum=state_enum,
        state_machine=state_machine,
    )
    bot = Bot(
        token=os.getenv("API_TOKEN"),
        queue_maxsize=int(os.getenv("QUEUE_MAX_SIZE")),
        queue_timeout=int(os.getenv("QUEUE_TIMEOUT")),
        update_timeout=int(os.getenv("UPDATES_TIMEOUT")),
        tg_api_url=os.getenv("TG_URL"),
        dispatcher=dispatcher,
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
