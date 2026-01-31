"""add category_id to products

Revision ID: 75032a9f2879
Revises: 54eaf1a3b16b
Create Date: 2026-01-31 13:57:34.220912

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '75032a9f2879'
down_revision: Union[str, None] = '54eaf1a3b16b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("products", sa.Column("category_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        "fk_products_category",
        "products",
        "categories",
        ["category_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_index("ix_products_category_id", "products", ["category_id"])


def downgrade() -> None:
    op.drop_index("ix_products_category_id", table_name="products")
    op.drop_constraint("fk_products_category", "products", type_="foreignkey")
    op.drop_column("products", "category_id")