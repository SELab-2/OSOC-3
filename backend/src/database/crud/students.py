from sqlalchemy.orm import Session
from src.database.enums import DecisionEnum
from src.database.models import Student


def get_student_by_id(db: Session, student_id: int) -> Student:
    """Get a student by id"""

    return db.query(Student).where(Student.student_id == student_id).one()


def set_definitive_decision_on_student(db: Session, student: Student, decision: DecisionEnum) -> None:
    """set a definitive decision on a student"""

    student.decision = decision
    db.commit()
