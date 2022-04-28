from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from src.database.crud.util import paginate
from src.database.enums import DecisionEnum, EmailStatusEnum
from src.database.models import Edition, Skill, Student, DecisionEmail
from src.app.schemas.students import CommonQueryParams, EmailsSearchQueryParams


def get_student_by_id(db: Session, student_id: int) -> Student:
    """Get a student by id"""

    return db.query(Student).where(Student.student_id == student_id).one()


def set_definitive_decision_on_student(db: Session, student: Student, decision: DecisionEnum) -> None:
    """set a definitive decision on a student"""

    student.decision = decision
    db.commit()


def delete_student(db: Session, student: Student) -> None:
    """Delete a student from the database"""
    db.delete(student)
    db.commit()


def get_students(db: Session, edition: Edition,
                 commons: CommonQueryParams, skills: list[Skill] = None) -> list[Student]:
    """Get students"""
    query = db.query(Student)\
        .where(Student.edition == edition)\
        .where((Student.first_name + ' ' + Student.last_name).contains(commons.name))\

    if commons.alumni:
        query = query.where(Student.alumni)

    if commons.student_coach:
        query = query.where(Student.wants_to_be_student_coach)

    if skills is None:
        skills = []

    for skill in skills:
        query = query.where(Student.skills.contains(skill))

    return paginate(query, commons.page).all()


def get_emails(db: Session, student: Student) -> list[DecisionEmail]:
    """Get all emails send to a student"""
    return db.query(DecisionEmail).where(DecisionEmail.student_id == student.student_id).all()


def create_email(db: Session, student: Student, email_status: EmailStatusEnum) -> DecisionEmail:
    """Create a new email in the database"""
    email: DecisionEmail = DecisionEmail(
        student=student, decision=email_status, date=datetime.now())
    db.add(email)
    db.commit()
    return email


def get_last_emails_of_students(db: Session, edition: Edition, commons: EmailsSearchQueryParams) -> list[DecisionEmail]:
    """get last email of all students that got an email"""
    last_emails = db.query(DecisionEmail.email_id, func.max(DecisionEmail.date))\
                    .join(Student)\
                    .where(Student.edition == edition)\
                    .where((Student.first_name + ' ' + Student.last_name).contains(commons.name))\
                    .group_by(DecisionEmail.student_id).subquery()

    emails = db.query(DecisionEmail).join(
                last_emails, DecisionEmail.email_id == last_emails.c.email_id
             )

    if commons.email_status:
        emails = emails.where(DecisionEmail.decision.in_(commons.email_status))

    emails = emails.order_by(DecisionEmail.student_id)
    return paginate(emails, commons.page).all()
