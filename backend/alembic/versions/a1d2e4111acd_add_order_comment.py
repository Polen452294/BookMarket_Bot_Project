"""add order comment

Revision ID: a1d2e4111acd
Revises: 81c49c73208d
Create Date: 2026-01-30 07:04:00.278826

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'a1d2e4111acd'
down_revision: Union[str, None] = '81c49c73208d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('orders', sa.Column('comment', sa.String(length=1024), nullable=True))


def downgrade() -> None:
    op.drop_column('orders', 'comment')
