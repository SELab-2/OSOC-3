from sqlalchemy.orm import Session
from src.database.enums import DecisionEnum
from src.database.models import Edition, Skill, Student, DecisionEmail
from src.app.schemas.students import CommonQueryParams


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
        .where(Student.first_name.contains(commons.first_name))\
        .where(Student.last_name.contains(commons.last_name))\

    if commons.alumni:
        query = query.where(Student.alumni)

    if commons.student_coach:
        query = query.where(Student.wants_to_be_student_coach)

    if skills is None:
        skills = []

    for skill in skills:
        query = query.where(Student.skills.contains(skill))

    return query.all()


def get_emails(db: Session, student: Student) -> list[DecisionEmail]:
    """Get all emails send to a student"""
    return db.query(DecisionEmail).where(DecisionEmail.student_id == student.student_id).all()
