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
from user_cache.cache.user_cache_impl import UserCache

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
    # Кэш
    Cache = UserCache()

    # Для БД
    connection_pool = await create_pool()
    TransactionManager = TransactionManagerImpl(connection_pool=connection_pool)

    # Все репозитории
    UserRepo = UserRepositoryImpl()
    IncomeRepository = IncomeRepositoryImpl()
    ExpenseRepository = ExpenseRepositoryImpl()
    IncomeCategoryRepository = IncomeCategoryRepositoryImpl()
    ExpenseCategoryRepository = ExpenseCategoryRepositoryImpl()

    # Сервисы
    IncomeService = IncomeServiceImpl(
        user_cache=Cache,
        transaction_manager=TransactionManager,
        user_repo=UserRepo,
        income_cat_repo=IncomeCategoryRepository,
        income_repo=IncomeRepository,
    )
    ExpenseService = ExpenseServiceImpl(
        user_cache=Cache,
        transaction_manager=TransactionManager,
        user_repo=UserRepo,
        expense_cat_repo=ExpenseCategoryRepository,
        expense_repo=ExpenseRepository,
    )
    UserService = UserServiceImpl(
        transaction_manager=TransactionManager,
        user_repo=UserRepo,
    )
    State_Enum = StateEnum(
        income_service=IncomeService,
        expense_service=ExpenseService,
        user_service=UserService,
        Inner_object=Inner,
    )
    State_Machine = StateMachine(
        income_service=IncomeService,
        expense_service=ExpenseService,
        user_service=UserService,
        state_enum=State_Enum,
    )
    dispatcher = Dispatcher(
        income_service=IncomeService,
        expense_service=ExpenseService,
        user_service=UserService,
        user_cache=Cache,
        state_enum=State_Enum,
        state_machine=State_Machine,
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
