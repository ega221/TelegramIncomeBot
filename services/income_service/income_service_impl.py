from services.interface import Service
from repository.user_repository.user_repository_impl import UserRepository
from repository.income_category_repository.income_category_repository_impl import IncomeCategoryRepository
from repository.income_repository.income_repository_impl import IncomeRepository


class IncomeService(Service):
    def __init__(self, user_repo: UserRepository, income_cat_repo: IncomeCategoryRepository,
                 income_repo: IncomeRepository):
        self.user_repo = user_repo
        self.expense_cat_repo = income_cat_repo
        self.expense_repo = income_repo
