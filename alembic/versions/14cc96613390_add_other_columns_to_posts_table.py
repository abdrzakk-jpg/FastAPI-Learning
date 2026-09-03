"""add other columns to `posts` Table

Revision ID: 14cc96613390
Revises: 265494c17708
Create Date: 2026-09-03 20:40:31.073429

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '14cc96613390'
down_revision: Union[str, Sequence[str], None] = '265494c17708'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()'), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'created_at')
    pass
