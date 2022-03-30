from sqlalchemy.orm import Session
from src.database.enums import DecisionEnum
from src.database.models import Edition, Skill, Student


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


def get_students(db: Session, edition: Edition ,first_name: str = "", last_name: str = "", alumni: bool = False, student_coach: bool = False, skills: list[Skill] = None) -> list[Student]:
    """Get students"""
    query = db.query(Student)\
        .where(Student.edition == edition)\
        .where(Student.first_name.contains(first_name))\
        .where(Student.last_name.contains(last_name))\

    if alumni:
        query = query.where(Student.alumni)

    if student_coach:
        query = query.where(Student.wants_to_be_student_coach)

    if skills is None:
        skills = []

    for skill in skills:
        query = query.where(Student.skills.contains(skill))

    return query.all()
