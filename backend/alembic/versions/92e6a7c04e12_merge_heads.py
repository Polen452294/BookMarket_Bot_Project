"""merge heads

Revision ID: 92e6a7c04e12
Revises: 4b9ada225219, d8e36a8b6765
Create Date: 2026-01-29 18:33:22.879888

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '92e6a7c04e12'
down_revision: Union[str, None] = ('4b9ada225219', 'd8e36a8b6765')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
