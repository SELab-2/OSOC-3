from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import func, and_

from src.app.schemas.students import CommonQueryParams, EmailsSearchQueryParams

from src.database.crud.util import paginate
from src.database.enums import DecisionEnum, EmailStatusEnum
from src.database.models import Edition, Skill, Student, DecisionEmail, Suggestion, User


async def get_student_by_id(db: AsyncSession, student_id: int) -> Student:
    """Get a student by id"""
    query = select(Student).where(Student.student_id == student_id)
    result = await db.execute(query)
    return result.unique().scalars().one()


async def set_definitive_decision_on_student(db: AsyncSession, student: Student, decision: DecisionEnum) -> None:
    """set a definitive decision on a student"""

    student.decision = decision
    await db.commit()


async def delete_student(db: AsyncSession, student: Student) -> None:
    """Delete a student from the database"""
    await db.delete(student)
    await db.commit()


async def get_students(db: AsyncSession, edition: Edition,
                       commons: CommonQueryParams, user: User, skills: list[Skill] = None) -> list[Student]:
    """Get students"""
    query = select(Student) \
        .where(Student.edition == edition) \
        .where((Student.first_name + ' ' + Student.last_name).contains(commons.name))

    if commons.alumni:
        query = query.where(Student.alumni)

    if commons.student_coach:
        query = query.where(Student.wants_to_be_student_coach)

    if commons.own_suggestions:
        subquery = select(Suggestion.student_id).where(Suggestion.coach == user)
        query = query.filter(Student.student_id.in_(subquery))

    if skills is None:
        skills = []

    for skill in skills:
        query = query.where(Student.skills.contains(skill))

    query = query.order_by(Student.first_name, Student.last_name)
    return (await db.execute(paginate(query, commons.page))).unique().scalars().all()


async def get_emails(db: AsyncSession, student: Student) -> list[DecisionEmail]:
    """Get all emails send to a student"""
    query = select(DecisionEmail).where(DecisionEmail.student_id == student.student_id)
    result = await db.execute(query)
    return result.unique().scalars().all()


async def create_email(db: AsyncSession, student: Student, email_status: EmailStatusEnum) -> DecisionEmail:
    """Create a new email in the database"""
    email: DecisionEmail = DecisionEmail(
        student=student, decision=email_status, date=datetime.now())
    db.add(email)
    await db.commit()
    return email


async def get_last_emails_of_students(db: AsyncSession, edition: Edition, commons: EmailsSearchQueryParams) -> list[
    DecisionEmail]:
    """get last email of all students that got an email"""
    last_emails = select(DecisionEmail.student_id, func.max(DecisionEmail.date).label("maxdate")) \
        .join(Student) \
        .where(Student.edition == edition) \
        .where((Student.first_name + ' ' + Student.last_name).contains(commons.name)) \
        .group_by(DecisionEmail.student_id).subquery()

    emails = select(DecisionEmail).join(
        last_emails, and_(DecisionEmail.student_id == last_emails.c.student_id,
                                  DecisionEmail.date == last_emails.c.maxdate)
    )

    if commons.email_status:
        emails = emails.where(DecisionEmail.decision.in_(commons.email_status))

    emails = emails.join(Student, DecisionEmail.student).order_by(Student.first_name, Student.last_name)
    return (await db.execute(paginate(emails, commons.page))).unique().scalars().all()
