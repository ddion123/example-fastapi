"""add content column to post table

Revision ID: 36557351897c
Revises: 5c7ece79d3cf
Create Date: 2022-01-12 11:44:23.114612

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36557351897c'
down_revision = '5c7ece79d3cf'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
