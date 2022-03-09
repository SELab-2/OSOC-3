"""Link invitation links to editions

Revision ID: b6a373574e13
Revises: 6433759fff33
Create Date: 2022-03-05 19:01:52.244338

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b6a373574e13'
down_revision = '6433759fff33'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('invite_links', schema=None) as batch_op:
        batch_op.add_column(sa.Column('edition_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('invite_links_editions_fk', 'editions', ['edition_id'], ['edition_id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('invite_links', schema=None) as batch_op:
        batch_op.drop_constraint('invite_links_editions_fk', type_='foreignkey')
        batch_op.drop_column('edition_id')

    # ### end Alembic commands ###