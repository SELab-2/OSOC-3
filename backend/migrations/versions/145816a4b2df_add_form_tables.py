"""Add Form tables

Revision ID: 145816a4b2df
Revises: 810c6967f5d5
Create Date: 2022-03-07 23:29:05.003945

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
import sqlalchemy_utils

# revision identifiers, used by Alembic.
revision = '145816a4b2df'
down_revision = '810c6967f5d5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'webhook_urls',
        sa.Column('webhook_id', sa.Integer(), nullable=False),
        sa.Column('uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=True),
        sa.Column('edition_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['edition_id'], ['editions.edition_id'], ),
        sa.PrimaryKeyConstraint('webhook_id')
    )
    op.create_table(
        'questions',
        sa.Column('question_id', sa.Integer(), nullable=False),
        sa.Column('type', sa.Enum(
            'CHECKBOXES', 'FILE_UPLOAD', 'INPUT_EMAIL', 'INPUT_LINK', 'INPUT_PHONE_NUMBER',
            'INPUT_TEXT', 'MULTIPLE_CHOICE', 'TEXTAREA', 'INPUT_NUMBER', name='questionenum'
        ), nullable=False),
        sa.Column('question', sa.Text(), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['student_id'], ['students.student_id'], ),
        sa.PrimaryKeyConstraint('question_id')
    )
    op.create_table(
        'question_answers',
        sa.Column('answer_id', sa.Integer(), nullable=False),
        sa.Column('answer', sa.Text(), nullable=True),
        sa.Column('question_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['question_id'], ['questions.question_id'], ),
        sa.PrimaryKeyConstraint('answer_id')
    )
    op.create_table(
        'question_file_answers',
        sa.Column('file_answer_id', sa.Integer(), nullable=False),
        sa.Column('file_name', sa.Text(), nullable=False),
        sa.Column('url', sa.Text(), nullable=False),
        sa.Column('mime_type', sa.Text(), nullable=False),
        sa.Column('size', sa.Integer(), nullable=False),
        sa.Column('question_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['question_id'], ['questions.question_id'], ),
        sa.PrimaryKeyConstraint('file_answer_id')
    )

    with op.batch_alter_table('students', schema=None) as batch_op:
        batch_op.add_column(sa.Column('first_name', sa.Text(), nullable=False))
        batch_op.add_column(sa.Column('last_name', sa.Text(), nullable=False))
        batch_op.add_column(sa.Column('preferred_name', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('edition_id', sa.Integer(), nullable=True))
        batch_op.drop_constraint('students_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'editions', ['edition_id'], ['edition_id'])
        batch_op.drop_column('cv_webhook_id')
        batch_op.drop_column('name')

    op.drop_table('webhooks')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('students', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', mysql.TEXT(), nullable=False))
        batch_op.add_column(
            sa.Column('cv_webhook_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('students_ibfk_1', 'webhooks', ['cv_webhook_id'], ['webhook_id'])
        batch_op.drop_column('edition_id')
        batch_op.drop_column('preferred_name')
        batch_op.drop_column('last_name')
        batch_op.drop_column('first_name')

    op.create_table('webhooks',
                    sa.Column('webhook_id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
                    sa.Column('edition_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
                    sa.ForeignKeyConstraint(['edition_id'], ['editions.edition_id'], name='webhooks_ibfk_1'),
                    sa.PrimaryKeyConstraint('webhook_id'),
                    mariadb_default_charset='latin1',
                    mariadb_engine='InnoDB'
                    )
    op.drop_table('question_file_answers')
    op.drop_table('question_answers')
    op.drop_table('questions')
    op.drop_table('webhook_urls')
    # ### end Alembic commands ###
