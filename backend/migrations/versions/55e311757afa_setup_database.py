"""Setup database

Revision ID: 55e311757afa
Revises: 
Create Date: 2022-05-22 13:34:31.251814

"""
import sqlalchemy as sa
import sqlalchemy_utils
from alembic import op

# revision identifiers, used by Alembic.
revision = '55e311757afa'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'editions',
        sa.Column('edition_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('readonly', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('edition_id'),
        sa.UniqueConstraint('name')
    )
    op.create_table(
        'partners',
        sa.Column('partner_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('partner_id'),
        sa.UniqueConstraint('name')
    )
    op.create_table(
        'skills',
        sa.Column('skill_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('skill_id')
    )
    op.create_table(
        'users',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('admin', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table(
        'coach_requests',
        sa.Column('request_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('edition_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['edition_id'], ['editions.edition_id'], name='coach_requests_editions_fk'),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], name='coach_requests_users_fk'),
        sa.PrimaryKeyConstraint('request_id')
    )
    op.create_table(
        'email_auths',
        sa.Column('email_auth_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('email', sa.Text(), nullable=False),
        sa.Column('pw_hash', sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], name='email_auths_users_fk'),
        sa.PrimaryKeyConstraint('email_auth_id'),
        sa.UniqueConstraint('email')
    )
    op.create_table(
        'github_auths',
        sa.Column('gh_auth_id', sa.Integer(), nullable=False),
        sa.Column('access_token', sa.Text(), nullable=True),
        sa.Column('email', sa.Text(), nullable=False),
        sa.Column('github_user_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], name='github_auths_users_fk'),
        sa.PrimaryKeyConstraint('gh_auth_id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('github_user_id')
    )
    op.create_table(
        'google_auths',
        sa.Column('google_auth_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('email', sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], name='google_auths_users_fk'),
        sa.PrimaryKeyConstraint('google_auth_id'),
        sa.UniqueConstraint('email')
    )
    op.create_table(
        'invite_links',
        sa.Column('invite_link_id', sa.Integer(), nullable=False),
        sa.Column('uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=True),
        sa.Column('target_email', sa.Text(), nullable=False),
        sa.Column('edition_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['edition_id'], ['editions.edition_id'], name='invite_links_editions_fk'),
        sa.PrimaryKeyConstraint('invite_link_id')
    )
    op.create_table(
        'projects',
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('info_url', sa.Text(), nullable=True),
        sa.Column('edition_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['edition_id'], ['editions.edition_id'], name='projects_editions_fk'),
        sa.PrimaryKeyConstraint('project_id')
    )
    op.create_table(
        'students',
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('first_name', sa.Text(), nullable=False),
        sa.Column('last_name', sa.Text(), nullable=False),
        sa.Column('preferred_name', sa.Text(), nullable=True),
        sa.Column('email_address', sa.Text(), nullable=False),
        sa.Column('phone_number', sa.Text(), nullable=True),
        sa.Column('alumni', sa.Boolean(), nullable=False),
        sa.Column('decision', sa.Enum('UNDECIDED', 'YES', 'MAYBE', 'NO', name='decisionenum'), nullable=True),
        sa.Column('wants_to_be_student_coach', sa.Boolean(), nullable=False),
        sa.Column('edition_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['edition_id'], ['editions.edition_id'], name='students_editions_fk'),
        sa.PrimaryKeyConstraint('student_id'),
        sa.UniqueConstraint('email_address'),
        sa.UniqueConstraint('phone_number')
    )
    op.create_table(
        'user_editions',
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('edition_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['edition_id'], ['editions.edition_id'], name='user_editions_editions_fk'),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], name='user_editions_users_fk')
    )
    op.create_table(
        'webhook_urls',
        sa.Column('webhook_id', sa.Integer(), nullable=False),
        sa.Column('uuid', sqlalchemy_utils.types.uuid.UUIDType(binary=False), nullable=True),
        sa.Column('edition_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['edition_id'], ['editions.edition_id'], name='webhook_urls_editions_fk'),
        sa.PrimaryKeyConstraint('webhook_id')
    )
    op.create_table(
        'decision_emails',
        sa.Column('email_id', sa.Integer(), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column(
            'decision',
            sa.Enum(
                'APPLIED',
                'AWAITING_PROJECT',
                'APPROVED',
                'CONTRACT_CONFIRMED',
                'CONTRACT_DECLINED',
                'REJECTED',
                name='emailstatusenum'
            ),
            nullable=False
        ),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['student_id'], ['students.student_id'], name='decision_emails_students_fk'),
        sa.PrimaryKeyConstraint('email_id')
    )
    op.create_table(
        'project_coaches',
        sa.Column('project_id', sa.Integer(), nullable=True),
        sa.Column('coach_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['coach_id'], ['users.user_id'], name='project_coaches_users_fk'),
        sa.ForeignKeyConstraint(['project_id'], ['projects.project_id'], name='project_coaches_projects_fk')
    )
    op.create_table(
        'project_partners',
        sa.Column('project_id', sa.Integer(), nullable=True),
        sa.Column('partner_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['partner_id'], ['partners.partner_id'], name='project_partners_partners_fk'),
        sa.ForeignKeyConstraint(['project_id'], ['projects.project_id'], name='project_partners_projects_fk')
    )
    op.create_table(
        'project_roles',
        sa.Column('project_role_id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=True),
        sa.Column('skill_id', sa.Integer(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('slots', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['projects.project_id'], name='project_roles_projects_fk'),
        sa.ForeignKeyConstraint(['skill_id'], ['skills.skill_id'], name='project_roles_skills_fk'),
        sa.PrimaryKeyConstraint('project_role_id')
    )
    op.create_table(
        'questions',
        sa.Column('question_id', sa.Integer(), nullable=False),
        sa.Column(
            'type',
            sa.Enum(
                'CHECKBOXES',
                'FILE_UPLOAD',
                'INPUT_EMAIL',
                'INPUT_LINK',
                'INPUT_PHONE_NUMBER',
                'INPUT_TEXT',
                'INPUT_NUMBER',
                'MULTIPLE_CHOICE',
                'TEXTAREA',
                'UNKNOWN',
                name='questionenum'
            ),
            nullable=False
        ),
        sa.Column('question', sa.Text(), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['student_id'], ['students.student_id'], name='questions_students_fk'),
        sa.PrimaryKeyConstraint('question_id')
    )
    op.create_table(
        'student_skills',
        sa.Column('student_id', sa.Integer(), nullable=True),
        sa.Column('skill_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['skill_id'], ['skills.skill_id'], name='student_skills_skills_fk'),
        sa.ForeignKeyConstraint(['student_id'], ['students.student_id'], name='student_skills_students_fk')
    )
    op.create_table(
        'suggestions',
        sa.Column('suggestion_id', sa.Integer(), nullable=False),
        sa.Column('student_id', sa.Integer(), nullable=False),
        sa.Column('coach_id', sa.Integer(), nullable=True),
        sa.Column('suggestion', sa.Enum('UNDECIDED', 'YES', 'MAYBE', 'NO', name='decisionenum'),
                  nullable=False),
        sa.Column('argumentation', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['coach_id'], ['users.user_id'], name='suggestions_users_fk'),
        sa.ForeignKeyConstraint(['student_id'], ['students.student_id'], name='suggestions_students_fk'),
        sa.PrimaryKeyConstraint('suggestion_id'),
        sa.UniqueConstraint('student_id', 'coach_id')
    )
    op.create_table(
        'pr_suggestions',
        sa.Column('project_role_suggestion_id', sa.Integer(), nullable=False),
        sa.Column('argumentation', sa.Text(), nullable=True),
        sa.Column('project_role_id', sa.Integer(), nullable=True),
        sa.Column('student_id', sa.Integer(), nullable=True),
        sa.Column('drafter_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['drafter_id'], ['users.user_id'], name='pr_suggestions_users_fk'),
        sa.ForeignKeyConstraint(
            ['project_role_id'],
            ['project_roles.project_role_id'],
            name='pr_suggestions_project_roles_fk'
        ),
        sa.ForeignKeyConstraint(['student_id'], ['students.student_id'], name='pr_suggestions_students_fk'),
        sa.PrimaryKeyConstraint('project_role_suggestion_id'),
        sa.UniqueConstraint('project_role_id', 'student_id')
    )
    op.create_table(
        'question_answers',
        sa.Column('answer_id', sa.Integer(), nullable=False),
        sa.Column('answer', sa.Text(), nullable=True),
        sa.Column('question_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['question_id'], ['questions.question_id'], name='question_answers_questions_fk'),
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
        sa.ForeignKeyConstraint(['question_id'], ['questions.question_id'], name='question_file_answers_questions_fk'),
        sa.PrimaryKeyConstraint('file_answer_id')
    )


def downgrade():
    op.drop_table('question_file_answers')
    op.drop_table('question_answers')
    op.drop_table('pr_suggestions')
    op.drop_table('suggestions')
    op.drop_table('student_skills')
    op.drop_table('questions')
    op.drop_table('project_roles')
    op.drop_table('project_partners')
    op.drop_table('project_coaches')
    op.drop_table('decision_emails')
    op.drop_table('webhook_urls')
    op.drop_table('user_editions')
    op.drop_table('students')
    op.drop_table('projects')
    op.drop_table('invite_links')
    op.drop_table('google_auths')
    op.drop_table('github_auths')
    op.drop_table('email_auths')
    op.drop_table('coach_requests')
    op.drop_table('users')
    op.drop_table('skills')
    op.drop_table('partners')
    op.drop_table('editions')
