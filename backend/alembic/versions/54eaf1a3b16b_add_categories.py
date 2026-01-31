"""add categories

Revision ID: 54eaf1a3b16b
Revises: a1d2e4111acd
Create Date: 2026-01-31 13:02:51.234513

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '54eaf1a3b16b'
down_revision: Union[str, None] = 'a1d2e4111acd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=100), nullable=False, unique=True),
    )


def downgrade() -> None:
    op.drop_table("categories")