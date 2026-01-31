"""add author and price to products

Revision ID: b34b75f6e290
Revises: 75032a9f2879
Create Date: 2026-01-31 17:39:35.570498

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'b34b75f6e290'
down_revision: Union[str, None] = '75032a9f2879'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column("products", sa.Column("author", sa.String(), nullable=True))
    op.add_column("products", sa.Column("price", sa.Integer(), nullable=True))

def downgrade():
    op.drop_column("products", "price")
    op.drop_column("products", "author")

