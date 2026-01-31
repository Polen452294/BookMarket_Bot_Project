"""add media bots broadcasts

Revision ID: d8e36a8b6765
Revises: db514357a021
Create Date: 2026-01-26 09:43:46.299348

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'd8e36a8b6765'
down_revision: Union[str, None] = 'db514357a021'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('bots',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('token', sa.String(length=256), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('broadcasts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(length=4096), nullable=False),
    sa.Column('status', sa.String(length=16), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('finished_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('broadcast_logs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('broadcast_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('bot_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(length=16), nullable=False),
    sa.Column('error_text', sa.String(length=1024), nullable=True),
    sa.Column('attempt', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['bot_id'], ['bots.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['broadcast_id'], ['broadcasts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_broadcast_logs_broadcast_id'), 'broadcast_logs', ['broadcast_id'], unique=False)
    op.create_index(op.f('ix_broadcast_logs_user_id'), 'broadcast_logs', ['user_id'], unique=False)
    op.create_table('media',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=16), nullable=False),
    sa.Column('url', sa.String(length=1024), nullable=False),
    sa.Column('sort_order', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_media_product_id'), 'media', ['product_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_media_product_id'), table_name='media')
    op.drop_table('media')
    op.drop_index(op.f('ix_broadcast_logs_user_id'), table_name='broadcast_logs')
    op.drop_index(op.f('ix_broadcast_logs_broadcast_id'), table_name='broadcast_logs')
    op.drop_table('broadcast_logs')
    op.drop_table('broadcasts')
    op.drop_table('bots')