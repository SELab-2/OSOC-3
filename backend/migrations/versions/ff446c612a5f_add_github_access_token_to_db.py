"""Add GitHub access token to db

Revision ID: ff446c612a5f
Revises: d4eaf2b564a4
Create Date: 2022-04-25 22:39:29.121923

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff446c612a5f'
down_revision = 'd4eaf2b564a4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('github_auths', schema=None) as batch_op:
        batch_op.add_column(sa.Column('access_token', sa.Text(), nullable=True))

        # Can't add a not-null field without a default value through migrations
        batch_op.add_column(sa.Column('github_user_id', sa.Integer(), nullable=False, server_default="-1"))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('github_auths', schema=None) as batch_op:
        batch_op.drop_column('access_token')
        batch_op.drop_column('github_user_id')

    # ### end Alembic commands ###
