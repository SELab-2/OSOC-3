from sqlalchemy.orm import Session

from src.app.schemas.students import NewDecision
from src.database.crud.students import set_definitive_decision_on_student, delete_student, get_students
from src.database.crud.skills import get_skills_by_ids
from src.database.models import Edition, Student, Skill
from src.app.schemas.students import ReturnStudentList, ReturnStudent, CommonQueryParams


def definitive_decision_on_student(db: Session, student: Student, decision: NewDecision) -> None:
    """Set a definitive decion on a student"""
    set_definitive_decision_on_student(db, student, decision.decision)


def remove_student(db: Session, student: Student) -> None:
    """delete a student"""
    delete_student(db, student)


def get_students_search(db: Session, edition: Edition, commons: CommonQueryParams) -> ReturnStudentList:
    """return all students"""
    if commons.skill_ids:
        skills: list[Skill] = get_skills_by_ids(db, commons.skill_ids)
        if len(skills) != len(commons.skill_ids):
            return ReturnStudentList(students=[])
    else:
        skills = []
    students = get_students(db, edition, first_name=commons.first_name,
                            last_name=commons.last_name, alumni=commons.alumni,
                            student_coach=commons.student_coach, skills=skills)
    return ReturnStudentList(students=students)


def get_student_return(student: Student) -> ReturnStudent:
    """return a student"""
    return ReturnStudent(student=student)
