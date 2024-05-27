from services.interface import Service
from repository.user_repository.user_repository_impl import UserRepository
from repository.expense_category_repository.expense_category_repository_impl import ExpenseCategoryRepository
from repository.expense_repository.expense_repository_impl import ExpenseRepository


class ExpenseService(Service):
    def __init__(self, user_repo: UserRepository, expense_cat_repo: ExpenseCategoryRepository,
                 expense_repo: ExpenseRepository):
        self.user_repo = user_repo
        self.expense_cat_repo = expense_cat_repo
        self.expense_repo = expense_repo
