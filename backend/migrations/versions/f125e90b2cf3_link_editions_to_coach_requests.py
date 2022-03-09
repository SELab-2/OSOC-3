"""link editions to coach requests

Revision ID: f125e90b2cf3
Revises: 73e669bda33d
Create Date: 2022-03-13 22:16:01.606059

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f125e90b2cf3'
down_revision = '73e669bda33d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('coach_requests', schema=None) as batch_op:
        batch_op.add_column(sa.Column('edition_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key("coach_requests_editions_fk", 'editions', ['edition_id'], ['edition_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('coach_requests', schema=None) as batch_op:
        batch_op.drop_constraint("coach_requests_editions_fk", type_='foreignkey')
        batch_op.drop_column('edition_id')

    # ### end Alembic commands ###