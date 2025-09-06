"""create votes table

Revision ID: bdf6a977ecd6
Revises: 1147f32b49df
Create Date: 2025-09-06 23:58:19.292836

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bdf6a977ecd6'
down_revision: Union[str, Sequence[str], None] = '1147f32b49df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('votes',
                    sa.Column('user_id', sa.INTEGER, nullable=False),
                    sa.Column('post_id', sa.INTEGER, nullable=False)
                    )
    pass


def downgrade() -> None:
    op.drop_table('votes')
    pass
