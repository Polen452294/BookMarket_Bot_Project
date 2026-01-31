"""create products

Revision ID: dff5275b87b7
Revises: 0001_create_products
Create Date: 2026-01-25 17:03:48.419182

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'dff5275b87b7'
down_revision: Union[str, None] = '0001_create_products'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
