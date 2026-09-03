"""Create `user` Table

Revision ID: 6b645c9903f7
Revises: 362e188ce1de
Create Date: 2026-09-03 11:29:06.828333

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6b645c9903f7'
down_revision: Union[str, Sequence[str], None] = '362e188ce1de'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'), #*=> equivalent to `unique=True`
        sa.UniqueConstraint('email') #*=> equivalent to `primary_key=True`
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
    pass
