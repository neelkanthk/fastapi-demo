"""Create users table

Revision ID: 8b98fccc52c5
Revises: 99a277c82944
Create Date: 2025-09-06 23:19:44.471118

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8b98fccc52c5'
down_revision: Union[str, Sequence[str], None] = '99a277c82944'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.INTEGER, primary_key=True),
                    sa.Column('email', sa.String(), nullable=False, unique=True),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default='now()'),
                    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=True)
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
