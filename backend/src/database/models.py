import enum

from sqlalchemy import Column, Integer, Enum, ForeignKey, Text, Boolean
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class RoleEnum(enum.Enum):
    """Enum for the different roles a user can have
    The actual value of the enum is NOT used in the database, only the name of the field
    """
    ADMIN = 0
    COACH = 1


class User(Base):
    """Users of the tool (only admins & coaches)"""
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    email = Column(Text, unique=True, nullable=False)
    role = Column(Enum(RoleEnum))

    coach_request = relationship("CoachRequest", uselist=False)


class CoachRequest(Base):
    """A request by somebody to become a coach, must be accepted by an admin
    This class doesn't hold an "accepted" state, because we remove the request
    once accepted or denied. If the request exists then it's still pending.
    """
    __tablename__ = "coach_requests"

    request_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)


class Partner(Base):
    """A partner working on a project, does not have access to the tool (or an account)"""
    __tablename__ = "partners"

    partner_id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)


class Skill(Base):
    """A skill a student can have, optionally with a description
    These skills are not unique per user, but can be shared among them as,
    for example, "Backend" can apply to anyone.

    Example:
        name:           Frontend
        description:    Must know React
    """
    __tablename__ = "skills"

    skill_id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    description = Column(Text, nullable=True, default=None)

    held_by = relationship("StudentSkill")


class Student(Base):
    """Information we have about a student"""
    __tablename__ = "students"

    student_id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    phone = Column(Text, nullable=True, default=None)
    alumni = Column(Boolean, nullable=False, default=False)

    skills = relationship("StudentSkill")


class StudentSkill(Base):
    """A skill possessed by a student
    Avoids having to use an Array type to store these in, which we want to avoid
    """
    __tablename__ = "student_skills"

    student_skill_id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.student_id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.skill_id"), nullable=False)


class Webhook(Base):
    """Data about a webhook for a student's CV that we've received"""
    __tablename__ = "webhooks"

    webhook_id = Column(Integer, primary_key=True)
