from sqlalchemy.orm import Session

from src.app.schemas.students import NewDecision
from src.database.crud.students import set_definitive_decision_on_student, delete_student, get_students
from src.database.models import Edition, Student
from src.app.schemas.students import ReturnStudentList, ReturnStudent

def definitive_decision_on_student(db: Session, student: Student, decision: NewDecision) -> None:
    """Set a definitive decion on a student"""
    set_definitive_decision_on_student(db, student, decision.decision)


def remove_student(db: Session, student: Student) -> None:
    """delete a student"""
    delete_student(db, student)


def get_students_search(db: Session, edition: Edition) -> ReturnStudentList:
    """return all students"""
    students = get_students(db, edition)
    return ReturnStudentList(students=students)


def get_student_return(student: Student) -> ReturnStudent:
    """return a student"""
    return ReturnStudent(student=student)
