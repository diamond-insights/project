"""Added column items_desc to Items table

Revision ID: 313d2e7eca59
Revises: 65dcacbd163c
Create Date: 2019-07-05 13:14:01.680987

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '313d2e7eca59'
down_revision = '65dcacbd163c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('items', sa.Column('item_desc', sa.String(length=255), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('items', 'item_desc')
    # ### end Alembic commands ###
