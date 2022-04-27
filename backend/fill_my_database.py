from src.database.engine import DBSession
from src.database.models import ProjectRole, project_partners, Suggestion, Project, Partner, InviteLink, DecisionEmail, \
    CoachRequest, student_skills, Student, Skill, user_editions, Edition, AuthGoogle, AuthEmail, User, AuthGitHub
from tests.fill_database import fill_database


session = DBSession()

for table in [ProjectRole, project_partners, Suggestion, Project, Partner, InviteLink, DecisionEmail,
              CoachRequest, student_skills, Student, Skill, user_editions, Edition, AuthGitHub, AuthGoogle,
              AuthEmail, User]:
    session.query(table).delete()

fill_database(session)