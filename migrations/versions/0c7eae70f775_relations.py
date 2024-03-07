"""relations

Revision ID: 0c7eae70f775
Revises: 7a78c54369fb
Create Date: 2024-03-07 19:22:34.270158

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0c7eae70f775'
down_revision: Union[str, None] = '7a78c54369fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_foreign_key(
        'fk_user_income_category',
        'income_categories',
        'users',
        ['user_id'],
        ['id'],
    )

    op.create_foreign_key(
        'fk_user_expense_category',
        'expense_categories',
        'users',
        ['user_id'],
        ['id'],
    )

    op.create_foreign_key(
        'fk_user_income',
        'incomes',
        'users',
        ['user_id'],
        ['id'],
    )

    op.create_foreign_key(
        'fk_user_expense',
        'expenses',
        'users',
        ['user_id'],
        ['id'],
    )

    op.create_foreign_key(
        'fk_income_category_income',
        'incomes',
        'income_categories',
        ['category_id'],
        ['id'],
    )

    op.create_foreign_key(
        'fk_expense_category_expense',
        'expenses',
        'expense_categories',
        ['category_id'],
        ['id'],
    )



def downgrade() -> None:
    op.drop_constraint(
        'fk_user_income_category',
        'income_categories',
    )

    op.drop_constraint(
        'fk_user_expense_category',
        'expense_categories',
    )

    op.drop_constraint(
        'fk_user_income',
        'incomes',
    )

    op.drop_constraint(
        'fk_user_expense',
        'expenses',
    )

    op.drop_constraint(
        'fk_income_category_income',
        'incomes',
    )

    op.drop_constraint(
        'fk_expense_category_expense',
        'expenses',
    )
