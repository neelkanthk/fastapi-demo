"""create posts table

Revision ID: 5140ead2ab56
Revises:
Create Date: 2025-09-06 20:07:36.344693

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import Column, INTEGER, VARCHAR, TEXT, BOOLEAN, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship


# revision identifiers, used by Alembic.
revision: str = '5140ead2ab56'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("posts", Column('id', INTEGER, primary_key=True, nullable=False),
                    Column('title', VARCHAR, nullable=False),
                    Column('content', TEXT, nullable=False),
                    Column('user_id', INTEGER, nullable=False),
                    Column('created_at', TIMESTAMP(timezone=True), nullable=False, server_default="now()"),
                    Column('updated_at', TIMESTAMP(timezone=True), nullable=True)
                    )
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
