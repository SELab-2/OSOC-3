from sqlalchemy import Column, Integer, Enum, ForeignKey, Text, Boolean, DateTime
from sqlalchemy.orm import declarative_base, relationship

from src.database.enums import RoleEnum, DecisionEnum

Base = declarative_base()


class User(Base):
    """Users of the tool (only admins & coaches)"""
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    email = Column(Text, unique=True, nullable=False)
    role = Column(Enum(RoleEnum), nullable=True)

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
    name = Column(Text, unique=True, nullable=False)


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

    held_by = relationship("StudentSkill", back_populates="skill")


class Student(Base):
    """Information we have about a student"""
    __tablename__ = "students"

    student_id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    email = Column(Text, unique=True, nullable=False)
    phone = Column(Text, unique=True, nullable=True, default=None)
    alumni = Column(Boolean, nullable=False, default=False)
    cv_webhook_id = Column(Integer, ForeignKey("webhooks.webhook_id"))
    decision = Column(Enum(DecisionEnum), nullable=True, default=DecisionEnum.UNDECIDED)
    wants_to_be_student_coach = Column(Boolean, nullable=False, default=False)

    emails = relationship("DecisionEmail")
    skills = relationship("StudentSkill", back_populates="student")
    webhook = relationship("Webhook", back_populates="student", uselist=False)


class StudentSkill(Base):
    """A skill possessed by a student
    Avoids having to use an Array type to store these in, which we want to avoid
    """
    __tablename__ = "student_skills"

    student_skill_id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.student_id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.skill_id"), nullable=False)

    student = relationship("Student", back_populates="skills")
    skill = relationship("Skill", back_populates="held_by")


class Webhook(Base):
    """Data about a webhook for a student's CV that we've received"""
    __tablename__ = "webhooks"

    webhook_id = Column(Integer, primary_key=True)

    student = relationship("Student", back_populates="webhook", uselist=False)


class DecisionEmail(Base):
    """An email sent out to a student that tells them the decision that was made"""
    __tablename__ = "decision_emails"

    email_id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.student_id"), nullable=False)
    decision = Column(Enum(DecisionEnum), nullable=False)
    date = Column(DateTime, nullable=False)
