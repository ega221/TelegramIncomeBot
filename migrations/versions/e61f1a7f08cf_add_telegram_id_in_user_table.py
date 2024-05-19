"""add_telegram_id_in_user_table

Revision ID: e61f1a7f08cf
Revises: 0c7eae70f775
Create Date: 2024-05-26 20:47:57.723801

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "e61f1a7f08cf"
down_revision: Union[str, None] = "0c7eae70f775"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("telegram_id", sa.Integer, nullable=False))


def downgrade() -> None:
    op.drop_column("users", "telegram_id")
