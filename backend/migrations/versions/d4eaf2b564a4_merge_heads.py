"""merge heads

Revision ID: d4eaf2b564a4
Revises: 43e6e98fe039, 1862d7dea4cc
Create Date: 2022-04-19 09:53:31.222511

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd4eaf2b564a4'
down_revision = ('43e6e98fe039', '1862d7dea4cc')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
