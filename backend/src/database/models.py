"""
All the database models and association tables

Association tables are tables that are only used to link two other
tables together using relationships, in order to avoid using an Array
"""
from sqlalchemy import Column, Integer, Enum, ForeignKey, Text, Boolean, DateTime
from sqlalchemy.orm import declarative_base, relationship

from src.database.enums import RoleEnum, DecisionEnum

Base = declarative_base()


class CoachRequest(Base):
    """A request by somebody to become a coach, must be accepted by an admin
    This class doesn't hold an "accepted" state, because we remove the request
    once accepted or denied. If the request exists then it's still pending.
    """
    __tablename__ = "coach_requests"

    request_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    user = relationship("User", back_populates="coach_request", uselist=False)


class DecisionEmail(Base):
    """An email sent out to a student that tells them the decision that was made"""
    __tablename__ = "decision_emails"

    email_id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.student_id"), nullable=False)
    decision = Column(Enum(DecisionEnum), nullable=False)
    date = Column(DateTime, nullable=False)

    student = relationship("Student", back_populates="emails", uselist=False)


class Partner(Base):
    """A partner working on a project, does not have access to the tool (or an account)"""
    __tablename__ = "partners"

    partner_id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True, nullable=False)

    projects = relationship("ProjectPartner", back_populates="partner")


class Project(Base):
    """A project of this edition"""
    __tablename__ = "projects"

    project_id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True, nullable=False)
    number_of_students = Column(Integer, nullable=False, default=0)
    edition = Column(Integer, nullable=False)

    coaches = relationship("ProjectCoach", back_populates="project")
    skills = relationship("ProjectSkill", back_populates="project")
    partners = relationship("ProjectPartner", back_populates="project")
    project_roles = relationship("ProjectRole", back_populates="project")


class ProjectCoach(Base):
    """A coach linked to a project
    Association table
    """
    __tablename__ = "project_coaches"

    project_id = Column(ForeignKey("projects.project_id"), primary_key=True)
    coach_id = Column(ForeignKey("users.user_id"), primary_key=True)

    project = relationship("Project", back_populates="coaches", uselist=False)
    coach = relationship("User", back_populates="projects", uselist=False)


class ProjectPartner(Base):
    """A partner linked to a project
    Association table
    """
    __tablename__ = "project_partners"

    project_id = Column(ForeignKey("projects.project_id"), primary_key=True)
    partner_id = Column(ForeignKey("partners.partner_id"), primary_key=True)

    partner = relationship("Partner", back_populates="projects")
    project = relationship("Project", back_populates="partners")


class ProjectRole(Base):
    """Skills fulfilled by a student in a given project
    Association table

    A ProjectRole is created when a coach (or admin) links a student to a project

    This differs from Project.skills in that Project.skills describes all the required skills,
    and doesn't have any users linked to them yet

    A student can have multiple project_roles before being assigned to a project, as they can
    be drafted for multiple projects
    """
    __tablename__ = "project_roles"

    student_id = Column(ForeignKey("students.student_id"), primary_key=True)
    project_id = Column(ForeignKey("projects.project_id"), primary_key=True)
    skill_id = Column(ForeignKey("skills.skill_id"), primary_key=True)
    definitive = Column(Boolean, nullable=False, default=False)
    argumentation = Column(Text, nullable=True)

    student = relationship("Student", back_populates="project_roles")
    project = relationship("Project", back_populates="project_roles")
    skill = relationship("Skill", back_populates="project_roles")


class ProjectSkill(Base):
    """A skill required by a project
    Association table
    """
    __tablename__ = "project_skills"

    project_id = Column(ForeignKey("projects.project_id"), primary_key=True)
    skill_id = Column(ForeignKey("skills.skill_id"), primary_key=True)

    project = relationship("Project", back_populates="skills", uselist=False)
    skill = relationship("Skill", back_populates="projects", uselist=False)


class Skill(Base):
    """A skill a student can have, optionally with a description
    These skills are not unique per user, but can be shared among them as,
    for example, "Backend" can apply to anyone.

    Example:
        name:        Frontend
        description: Must know React
    """
    __tablename__ = "skills"

    skill_id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=True)

    project_roles = relationship("ProjectRole", back_populates="skill")
    projects = relationship("ProjectSkill", back_populates="skill")


class Student(Base):
    """Information we have about a student"""
    __tablename__ = "students"

    student_id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    email_address = Column(Text, unique=True, nullable=False)
    phone_number = Column(Text, unique=True, nullable=True, default=None)
    alumni = Column(Boolean, nullable=False, default=False)
    cv_webhook_id = Column(Integer, ForeignKey("webhooks.webhook_id"))
    decision = Column(Enum(DecisionEnum), nullable=True, default=DecisionEnum.UNDECIDED)
    wants_to_be_student_coach = Column(Boolean, nullable=False, default=False)

    emails = relationship("DecisionEmail", back_populates="student")
    project_roles = relationship("ProjectRole", back_populates="student")
    suggestions = relationship("Suggestion", back_populates="student")
    webhook = relationship("Webhook", back_populates="student", uselist=False)


class Suggestion(Base):
    """A suggestion left by a coach about a student"""
    __tablename__ = "suggestions"

    suggestion_id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.student_id"), nullable=False)
    coach_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    suggestion = Column(Enum(DecisionEnum), nullable=False, default=DecisionEnum.UNDECIDED)
    argumentation = Column(Text, nullable=True)

    student = relationship("Student", back_populates="suggestions", uselist=False)
    coach = relationship("Users", back_populates="suggestions", uselist=False)


class User(Base):
    """Users of the tool (only admins & coaches)"""
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    email = Column(Text, unique=True, nullable=False)
    role = Column(Enum(RoleEnum), nullable=True)

    coach_request = relationship("CoachRequest", back_populates="user", uselist=False)
    projects = relationship("ProjectCoach", back_populates="coach")
    suggestions = relationship("Suggestion", back_populates="user")


class Webhook(Base):
    """Data about a webhook for a student's CV that we've received"""
    __tablename__ = "webhooks"

    webhook_id = Column(Integer, primary_key=True)

    student = relationship("Student", back_populates="webhook", uselist=False)
