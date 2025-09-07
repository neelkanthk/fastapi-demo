"""add is_verified column in users table

Revision ID: 318b8cba2970
Revises: 5c2df512c47f
Create Date: 2025-09-07 11:28:43.343011

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '318b8cba2970'
down_revision: Union[str, Sequence[str], None] = '5c2df512c47f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('is_verified', sa.BOOLEAN, nullable=False, server_default='FALSE'))


def downgrade() -> None:
    op.drop_column('users', 'is_verified')
