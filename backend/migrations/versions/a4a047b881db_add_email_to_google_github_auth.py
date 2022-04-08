"""Add email to Google & GitHub auth

Revision ID: a4a047b881db
Revises: a5f19eb19cca
Create Date: 2022-04-06 17:40:15.305860

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4a047b881db'
down_revision = 'a5f19eb19cca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('github_auths', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.Text(), nullable=False))
        batch_op.create_unique_constraint("uq_github_auths_email", ['email'])

    with op.batch_alter_table('google_auths', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.Text(), nullable=False))
        batch_op.create_unique_constraint("uq_google_auths_email", ['email'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('google_auths', schema=None) as batch_op:
        batch_op.drop_constraint("uq_google_auths_email", type_='unique')
        batch_op.drop_column('email')

    with op.batch_alter_table('github_auths', schema=None) as batch_op:
        batch_op.drop_constraint("uq_github_auths_email", type_='unique')
        batch_op.drop_column('email')

    # ### end Alembic commands ###
