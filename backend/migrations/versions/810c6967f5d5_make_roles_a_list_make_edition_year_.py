"""Make roles a list, make edition year unique

Revision ID: 810c6967f5d5
Revises: d29dfe421181
Create Date: 2022-03-06 15:07:34.230577

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '810c6967f5d5'
down_revision = 'd29dfe421181'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('editions', schema=None) as batch_op:
        batch_op.create_unique_constraint("uq_editions_year", ['year'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('editions', schema=None) as batch_op:
        batch_op.drop_constraint("uq_editions_year", type_='unique')

    # ### end Alembic commands ###