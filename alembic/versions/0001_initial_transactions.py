"""initial

Revision ID: 0001_initial_transactions
Revises: 
Create Date: 2026-01-01 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_initial_transactions'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'transactions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('date', sa.Date(), nullable=True),
        sa.Column('description', sa.String(length=512), nullable=True),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('category', sa.String(length=128), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # initial table creation


def downgrade():
    op.drop_table('transactions')
