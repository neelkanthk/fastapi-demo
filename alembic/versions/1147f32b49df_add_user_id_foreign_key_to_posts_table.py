"""add user_id foreign key to posts table

Revision ID: 1147f32b49df
Revises: 8b98fccc52c5
Create Date: 2025-09-06 23:40:55.780055

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1147f32b49df'
down_revision: Union[str, Sequence[str], None] = '8b98fccc52c5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_foreign_key('posts_user_fkey', source_table='posts', referent_table='users',
                          local_cols=['user_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('posts_user_fkey', table_name='posts')
    pass
