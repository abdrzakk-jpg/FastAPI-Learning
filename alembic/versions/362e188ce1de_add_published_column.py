"""Add `published` column

Revision ID: 362e188ce1de
Revises: 4fed3ad44a72
Create Date: 2026-09-03 11:20:09.056112

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '362e188ce1de'
down_revision: Union[str, Sequence[str], None] = '4fed3ad44a72'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    #! create published column
    op.add_column(
        'posts', 
        sa.Column('published', sa.Boolean(), nullable=False, default=sa.false())
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'published')
    pass
