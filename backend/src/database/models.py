"""
All the database models and association tables

Association tables are tables that are only used to link two other
tables together using relationships, in order to avoid using an Array
more info: https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#association-object

Relationships are not literally stored in the database: these are
implicit fields that can be generated if necessary by linking data
together
"""
from __future__ import annotations

from uuid import uuid4, UUID

from sqlalchemy import Column, Integer, Enum, ForeignKey, Text, Boolean, DateTime, Table, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy_utils import UUIDType  # type: ignore

from src.database.enums import DecisionEnum, EmailStatusEnum, QuestionEnum

Base = declarative_base()


class AuthEmail(Base):
    """Authentication data for email/password"""
    __tablename__ = "email_auths"

    email_auth_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    email = Column(Text, unique=True, nullable=False)
    pw_hash = Column(Text, nullable=False)

    user: User = relationship("User", back_populates="email_auth", uselist=False)


class AuthGitHub(Base):
    """Authentication data for GitHub"""
    __tablename__ = "github_auths"

    gh_auth_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    email = Column(Text, unique=True, nullable=False)

    user: User = relationship("User", back_populates="github_auth", uselist=False)


class AuthGoogle(Base):
    """Authentication data for Google"""
    __tablename__ = "google_auths"

    google_auth_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    email = Column(Text, unique=True, nullable=False)

    user: User = relationship("User", back_populates="google_auth", uselist=False)


class CoachRequest(Base):
    """A request by somebody to become a coach, must be accepted by an admin
    This class doesn't hold an "accepted" state, because we remove the request
    once accepted or denied. If the request exists then it's still pending.
    """
    __tablename__ = "coach_requests"

    request_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    edition_id = Column(Integer, ForeignKey("editions.edition_id"), nullable=False)

    edition: Edition = relationship("Edition", back_populates="coach_requests", uselist=False)
    user: User = relationship("User", back_populates="coach_request", uselist=False)


class DecisionEmail(Base):
    """An email sent out to a student that tells them the decision that was made"""
    __tablename__ = "decision_emails"

    email_id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.student_id"), nullable=False)
    decision = Column(Enum(EmailStatusEnum), nullable=False)
    date = Column(DateTime, nullable=False)

    student: Student = relationship("Student", back_populates="emails", uselist=False, lazy="joined")


class Edition(Base):
    """An edition of the tool, to link other resources to"""
    __tablename__ = "editions"

    edition_id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True, nullable=False)
    year = Column(Integer, unique=True, nullable=False)

    invite_links: list[InviteLink] = relationship("InviteLink", back_populates="edition")
    projects: list[Project] = relationship("Project", back_populates="edition")
    coaches: list[User] = relationship("User", secondary="user_editions", back_populates="editions")
    coach_requests: list[CoachRequest] = relationship("CoachRequest", back_populates="edition")
    students: list[Student] = relationship("Student", back_populates="edition")
    webhook_urls: list[WebhookURL] = relationship("WebhookURL", back_populates="edition")


class InviteLink(Base):
    """A unique invite link sent to a user in order to create an account"""
    __tablename__ = "invite_links"

    invite_link_id = Column(Integer, primary_key=True)
    uuid: UUID = Column(UUIDType(binary=False), default=uuid4)
    target_email = Column(Text, nullable=False)
    edition_id = Column(Integer, ForeignKey("editions.edition_id", name="fk_invite_link_edition_id_edition"))

    edition: Edition = relationship("Edition", back_populates="invite_links", uselist=False)


class Partner(Base):
    """A partner working on a project, does not have access to the tool (or an account)"""
    __tablename__ = "partners"

    partner_id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True, nullable=False)

    projects: list[Project] = relationship("Project", secondary="project_partners", back_populates="partners")


class Project(Base):
    """A project of this edition"""
    __tablename__ = "projects"

    project_id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    number_of_students = Column(Integer, nullable=False, default=0)
    edition_id = Column(Integer, ForeignKey("editions.edition_id"))

    edition: Edition = relationship("Edition", back_populates="projects", uselist=False, lazy="joined")
    coaches: list[User] = relationship("User", secondary="project_coaches", back_populates="projects", lazy="joined")
    skills: list[Skill] = relationship("Skill", secondary="project_skills", back_populates="projects", lazy="joined")
    partners: list[Partner] = relationship("Partner", secondary="project_partners", back_populates="projects", lazy="joined")
    project_roles: list[ProjectRole] = relationship("ProjectRole", back_populates="project", lazy="joined", cascade="save-update, merge, delete, delete-orphan")


project_coaches = Table(
    "project_coaches", Base.metadata,
    Column("project_id", ForeignKey("projects.project_id")),
    Column("coach_id", ForeignKey("users.user_id"))
)

project_partners = Table(
    "project_partners", Base.metadata,
    Column("project_id", ForeignKey("projects.project_id")),
    Column("partner_id", ForeignKey("partners.partner_id"))
)


class ProjectRole(Base):
    """Skills fulfilled by a student in a given project
    Association table

    A ProjectRole is created when a coach (or admin) links a student to a project

    This differs from project_skills in that project_skills describes all the required skills
    for a project, and doesn't have any users linked to them yet

    A student can have multiple ProjectRoles before being assigned to a project, as they can
    be drafted for multiple projects
    """
    __tablename__ = "project_roles"

    student_id = Column(Integer, ForeignKey("students.student_id"), primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.project_id"), primary_key=True)
    skill_id = Column(Integer, ForeignKey("skills.skill_id"), primary_key=True)
    definitive = Column(Boolean, nullable=False, default=False)
    argumentation = Column(Text, nullable=True)
    drafter_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    student: Student = relationship("Student", back_populates="project_roles", uselist=False)
    project: Project = relationship("Project", back_populates="project_roles", uselist=False)
    skill: Skill = relationship("Skill", back_populates="project_roles", uselist=False)
    drafter: User = relationship("User", back_populates="drafted_roles", uselist=False)


project_skills = Table(
    "project_skills", Base.metadata,
    Column("project_id", ForeignKey("projects.project_id")),
    Column("skill_id", ForeignKey("skills.skill_id"))
)


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

    project_roles: list[ProjectRole] = relationship("ProjectRole", back_populates="skill")
    projects: list[Project] = relationship("Project", secondary="project_skills", back_populates="skills")
    students: list[Student] = relationship("Student", secondary="student_skills", back_populates="skills")


class Student(Base):
    """Information we have about a student"""
    __tablename__ = "students"

    student_id = Column(Integer, primary_key=True)
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)
    preferred_name = Column(Text)
    email_address = Column(Text, unique=True, nullable=False)
    phone_number = Column(Text, unique=True, nullable=True, default=None)
    alumni = Column(Boolean, nullable=False, default=False)
    # cv_url = Column(Text)
    decision = Column(Enum(DecisionEnum), nullable=True, default=DecisionEnum.UNDECIDED)
    wants_to_be_student_coach = Column(Boolean, nullable=False, default=False)
    edition_id = Column(Integer, ForeignKey("editions.edition_id"))

    emails: list[DecisionEmail] = relationship("DecisionEmail", back_populates="student", cascade="all, delete-orphan", lazy="joined")
    project_roles: list[ProjectRole] = relationship("ProjectRole", back_populates="student", lazy="joined")
    skills: list[Skill] = relationship("Skill", secondary="student_skills", back_populates="students", lazy="joined")
    suggestions: list[Suggestion] = relationship("Suggestion", back_populates="student", lazy="joined")
    questions: list[Question] = relationship("Question", back_populates="student", lazy="joined")
    edition: Edition = relationship("Edition", back_populates="students", uselist=False, lazy="joined")


class Question(Base):
    """A question from the form"""
    __tablename__ = "questions"

    question_id = Column(Integer, primary_key=True)
    type = Column(Enum(QuestionEnum), nullable=False)
    question = Column(Text, nullable=False)
    student_id = Column(Integer, ForeignKey("students.student_id"), nullable=False)

    answers: list[QuestionAnswer] = relationship("QuestionAnswer", back_populates="question")
    files: list[QuestionFileAnswer] = relationship("QuestionFileAnswer", back_populates="question")
    student: Student = relationship("Student", back_populates="questions", uselist=False)


class QuestionAnswer(Base):
    """Answer on a question for the form"""
    __tablename__ = "question_answers"

    answer_id = Column(Integer, primary_key=True)
    answer = Column(Text, nullable=True)
    question_id = Column(Integer, ForeignKey("questions.question_id"), nullable=False)

    question: Question = relationship("Question", back_populates="answers", uselist=False)


class QuestionFileAnswer(Base):
    """An answer containg a file"""
    __tablename__ = "question_file_answers"

    file_answer_id = Column(Integer, primary_key=True)
    file_name = Column(Text, nullable=False)
    url = Column(Text, nullable=False)
    mime_type = Column(Text, nullable=False)
    size = Column(Integer, nullable=False)
    question_id = Column(Integer, ForeignKey("questions.question_id"), nullable=False)

    question: Question = relationship("Question", back_populates="files", uselist=False)


student_skills = Table(
    "student_skills", Base.metadata,
    Column("student_id", ForeignKey("students.student_id")),
    Column("skill_id", ForeignKey("skills.skill_id"))
)


class Suggestion(Base):
    """A suggestion left by a coach about a student"""
    __tablename__ = "suggestions"
    __table_args__=(
        UniqueConstraint('coach_id', 'student_id', name='unique_coach_student_suggestion'),
    )

    suggestion_id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.student_id"), nullable=False)
    coach_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    suggestion = Column(Enum(DecisionEnum), nullable=False, default=DecisionEnum.UNDECIDED)
    argumentation = Column(Text, nullable=True)

    student: Student = relationship("Student", back_populates="suggestions", uselist=False, lazy="joined")
    coach: User = relationship("User", back_populates="suggestions", uselist=False, lazy="joined")


class User(Base):
    """Users of the tool (only admins & coaches)"""
    __tablename__ = "users"

    user_id: int = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    admin = Column(Boolean, nullable=False, default=False)

    coach_request: CoachRequest = relationship("CoachRequest", back_populates="user", uselist=False, lazy="joined")
    drafted_roles: list[ProjectRole] = relationship("ProjectRole", back_populates="drafter", lazy="joined")
    editions: list[Edition] = relationship("Edition", secondary="user_editions", back_populates="coaches", lazy="joined")
    projects: list[Project] = relationship("Project", secondary="project_coaches", back_populates="coaches", lazy="joined")
    suggestions: list[Suggestion] = relationship("Suggestion", back_populates="coach", lazy="joined")

    # Authentication methods
    email_auth: AuthEmail = relationship("AuthEmail", back_populates="user", uselist=False, lazy="joined")
    github_auth: AuthGitHub = relationship("AuthGitHub", back_populates="user", uselist=False, lazy="joined")
    google_auth: AuthGoogle = relationship("AuthGoogle", back_populates="user", uselist=False, lazy="joined")


user_editions = Table(
    "user_editions", Base.metadata,
    Column("user_id", ForeignKey("users.user_id")),
    Column("edition_id", ForeignKey("editions.edition_id"))
)


class WebhookURL(Base):
    """Allowed webhook uuid's"""
    __tablename__ = "webhook_urls"

    webhook_id = Column(Integer, primary_key=True)
    uuid: UUID = Column(UUIDType(binary=False), default=uuid4)
    edition_id = Column(Integer, ForeignKey("editions.edition_id"))

    edition: Edition = relationship("Edition", back_populates="webhook_urls", uselist=False)
