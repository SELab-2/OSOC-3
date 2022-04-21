from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from src.app.exceptions.students_email import FailedToAddNewEmailException
from src.app.schemas.students import NewDecision
from src.database.crud.skills import get_skills_by_ids
from src.database.crud.students import (get_last_emails_of_students, get_student_by_id,
                                        set_definitive_decision_on_student,
                                        delete_student, get_students, get_emails,
                                        create_email)
from src.database.crud.suggestions import get_suggestions_of_student_by_type
from src.database.enums import DecisionEnum
from src.database.models import Edition, Student, Skill, DecisionEmail
from src.app.schemas.students import (
    ReturnStudentList, ReturnStudent, CommonQueryParams, ReturnStudentMailList,
    Student as StudentModel, Suggestions as SuggestionsModel,
    NewEmail, DecisionEmail as DecionEmailModel, EmailsSearchQueryParams)


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
    students_orm = get_students(db, edition, commons, skills)

    students: list[StudentModel] = []
    for student in students_orm:
        students.append(StudentModel(
            student_id=student.student_id,
            first_name=student.first_name,
            last_name=student.last_name,
            preferred_name=student.preferred_name,
            email_address=student.email_address,
            phone_number=student.phone_number,
            alumni=student.alumni,
            finalDecision=student.decision,
            wants_to_be_student_coach=student.wants_to_be_student_coach,
            edition_id=student.edition_id,
            skills=student.skills))
        nr_of_yes_suggestions = len(get_suggestions_of_student_by_type(
            db, student.student_id, DecisionEnum.YES))
        nr_of_no_suggestions = len(get_suggestions_of_student_by_type(
            db, student.student_id, DecisionEnum.NO))
        nr_of_maybe_suggestions = len(get_suggestions_of_student_by_type(
            db, student.student_id, DecisionEnum.MAYBE))
        students[-1].nr_of_suggestions = SuggestionsModel(
            yes=nr_of_yes_suggestions, no=nr_of_no_suggestions, maybe=nr_of_maybe_suggestions)
    return ReturnStudentList(students=students)


def get_student_return(student: Student, edition: Edition) -> ReturnStudent:
    """return a student"""
    if student.edition == edition:
        return ReturnStudent(student=student)

    raise NoResultFound


def get_emails_of_student(db: Session, edition: Edition, student: Student) -> ReturnStudentMailList:
    """returns all mails of a student"""
    if student.edition != edition:
        raise NoResultFound
    emails: list[DecisionEmail] = get_emails(db, student)
    return ReturnStudentMailList(emails=emails)


def make_new_email(db: Session, edition: Edition, new_email: NewEmail) -> DecionEmailModel:
    """make a new email"""
    student = get_student_by_id(db, new_email.student_id)
    if student.edition != edition:
        raise FailedToAddNewEmailException
    email: DecisionEmail = create_email(db, student, new_email.email_status)
    return email


def last_emails_of_students(db: Session, edition: Edition, commons: EmailsSearchQueryParams) -> ReturnStudentMailList:
    """get last emails of students with search params"""
    emails: list[DecisionEmail] = get_last_emails_of_students(db, edition, commons)
    return ReturnStudentMailList(emails=emails)
