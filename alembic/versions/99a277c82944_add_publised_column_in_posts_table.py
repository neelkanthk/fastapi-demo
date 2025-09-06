"""add publised column in posts table

Revision ID: 99a277c82944
Revises: 5140ead2ab56
Create Date: 2025-09-06 20:27:23.611639

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '99a277c82944'
down_revision: Union[str, Sequence[str], None] = '5140ead2ab56'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.BOOLEAN, nullable=False,
                  server_default='TRUE'))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    pass
