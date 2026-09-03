"""Add `author_id` FK

Revision ID: 265494c17708
Revises: 6b645c9903f7
Create Date: 2026-09-03 20:24:36.570419

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '265494c17708'
down_revision: Union[str, Sequence[str], None] = '6b645c9903f7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('author_id', sa.Integer(), nullable=False,))
    op.create_foreign_key(
        constraint_name='posts_user_fk', 
        source_table='posts', #* FROM posts|----
        referent_table='users', #* TO ---->users
        local_cols=["author_id"], #* bcoz now i'm in source_table
        remote_cols=["id"],
        ondelete='CASCADE'
        )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('posts_user_fk', table_name='posts', type_='foreignkey')
    op.drop_column('posts', 'author_id')
    pass
