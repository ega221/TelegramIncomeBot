"""initial

Revision ID: 7a78c54369fb
Revises: 
Create Date: 2024-03-07 15:17:34.286726

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7a78c54369fb"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
    )

    op.create_table(
        "income_categories",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.Integer),
        sa.Column("category_name", sa.Unicode(100)),
    )

    op.create_table(
        "expense_categories",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.Integer),
        sa.Column("category_name", sa.Unicode(100)),
    )

    op.create_table(
        "incomes",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("category_id", sa.Integer),
        sa.Column("user_id", sa.Integer),
        sa.Column("value", sa.Integer),
        sa.Column("date", sa.Date),
    )

    op.create_table(
        "expenses",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("category_id", sa.Integer),
        sa.Column("user_id", sa.Integer),
        sa.Column("value", sa.Integer),
        sa.Column("date", sa.Date),
    )


def downgrade() -> None:
    op.drop_table("users")
    op.drop_table("income_categories")
    op.drop_table("expense_categories")
    op.drop_table("incomes")
    op.drop_table("expenses")
    pass
