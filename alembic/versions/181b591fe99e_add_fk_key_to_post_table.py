"""add fk key to post table

Revision ID: 181b591fe99e
Revises: 4d5c0957ecda
Create Date: 2022-01-12 13:06:34.518619

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '181b591fe99e'
down_revision = '4d5c0957ecda'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
