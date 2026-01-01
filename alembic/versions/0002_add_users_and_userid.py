"""add users table and user_id on transactions

Revision ID: 0002_add_users_and_userid
Revises: 0001_initial_transactions
Create Date: 2026-01-01 00:30:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0002_add_users_and_userid'
down_revision = '0001_initial_transactions'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('username', sa.String(length=150), nullable=False, unique=True),
        sa.Column('email', sa.String(length=320), nullable=True, unique=True),
        sa.Column('hashed_password', sa.String(length=256), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.add_column('transactions', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_transactions_user', 'transactions', 'users', ['user_id'], ['id'])
    op.create_index(op.f('ix_transactions_user_id'), 'transactions', ['user_id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_transactions_user_id'), table_name='transactions')
    op.drop_constraint('fk_transactions_user', 'transactions', type_='foreignkey')
    op.drop_column('transactions', 'user_id')
    op.drop_table('users')
