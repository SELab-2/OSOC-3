import pytest
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.database.models import Suggestion, Student, User

from src.database.crud.suggestions import create_suggestion, get_suggestions_of_student, get_suggestion_by_id
from tests.fill_database import fill_database
from src.database.enums import DecisionEnum
from sqlalchemy.orm.exc import NoResultFound

def test_create_suggestion_yes(database_session: Session):
    fill_database(database_session)

    user: User = database_session.query(User).where(User.name == "coach1").first()
    student: Student = database_session.query(Student).where(Student.email_address == "marta.marquez@example.com").first()
    
    create_suggestion(database_session, user.user_id, student.student_id, DecisionEnum.YES, "This is a good student")

    suggestion: Suggestion = database_session.query(Suggestion).where(Suggestion.coach == user).where(Suggestion.student_id == student.student_id).one()

    assert suggestion.coach == user
    assert suggestion.student == student
    assert suggestion.suggestion == DecisionEnum.YES
    assert suggestion.argumentation == "This is a good student"

def test_create_suggestion_no(database_session: Session):
    fill_database(database_session)

    user: User = database_session.query(User).where(User.name == "coach1").first()
    student: Student = database_session.query(Student).where(Student.email_address == "marta.marquez@example.com").first()
    
    create_suggestion(database_session, user.user_id, student.student_id, DecisionEnum.NO, "This is a not good student")

    suggestion: Suggestion = database_session.query(Suggestion).where(Suggestion.coach == user).where(Suggestion.student_id == student.student_id).one()

    assert suggestion.coach == user
    assert suggestion.student == student
    assert suggestion.suggestion == DecisionEnum.NO
    assert suggestion.argumentation == "This is a not good student"

def test_create_suggestion_maybe(database_session: Session):
    fill_database(database_session)

    user: User = database_session.query(User).where(User.name == "coach1").first()
    student: Student = database_session.query(Student).where(Student.email_address == "marta.marquez@example.com").first()
    
    create_suggestion(database_session, user.user_id, student.student_id, DecisionEnum.MAYBE, "Idk if it's good student")

    suggestion: Suggestion = database_session.query(Suggestion).where(Suggestion.coach == user).where(Suggestion.student_id == student.student_id).one()

    assert suggestion.coach == user
    assert suggestion.student == student
    assert suggestion.suggestion == DecisionEnum.MAYBE
    assert suggestion.argumentation == "Idk if it's good student"

def test_one_coach_two_students(database_session: Session):
    fill_database(database_session)

    user: User = database_session.query(User).where(User.name == "coach1").one()
    student1: Student = database_session.query(Student).where(Student.email_address == "marta.marquez@example.com").one()
    student2: Student = database_session.query(Student).where(Student.email_address == "sofia.haataja@example.com").one()
    
    create_suggestion(database_session, user.user_id, student1.student_id, DecisionEnum.YES, "This is a good student")
    create_suggestion(database_session, user.user_id, student2.student_id, DecisionEnum.NO, "This is a not good student")

    suggestion1: Suggestion = database_session.query(Suggestion).where(Suggestion.coach == user).where(Suggestion.student_id == student1.student_id).one()
    assert suggestion1.coach == user
    assert suggestion1.student == student1
    assert suggestion1.suggestion == DecisionEnum.YES
    assert suggestion1.argumentation == "This is a good student"

    suggestion2: Suggestion = database_session.query(Suggestion).where(Suggestion.coach == user).where(Suggestion.student_id == student2.student_id).one()
    assert suggestion2.coach == user
    assert suggestion2.student == student2
    assert suggestion2.suggestion == DecisionEnum.NO
    assert suggestion2.argumentation == "This is a not good student"

def test_multiple_suggestions_about_same_student(database_session: Session):
    fill_database(database_session)

    user: User = database_session.query(User).where(User.name == "coach1").first()
    student: Student = database_session.query(Student).where(Student.email_address == "marta.marquez@example.com").first()
    
    create_suggestion(database_session, user.user_id, student.student_id, DecisionEnum.MAYBE, "Idk if it's good student")
    with pytest.raises(IntegrityError):
        create_suggestion(database_session, user.user_id, student.student_id, DecisionEnum.YES, "This is a good student")
    
def test_get_suggestions_of_student(database_session: Session):
    fill_database(database_session)

    user1: User = database_session.query(User).where(User.name == "coach1").first()
    user2: User = database_session.query(User).where(User.name == "coach2").first()
    student: Student = database_session.query(Student).where(Student.email_address == "marta.marquez@example.com").first()
    
    create_suggestion(database_session, user1.user_id, student.student_id, DecisionEnum.MAYBE, "Idk if it's good student")
    create_suggestion(database_session, user2.user_id, student.student_id, DecisionEnum.YES, "This is a good student")
    suggestions_student = get_suggestions_of_student(database_session, student.student_id)
    
    assert len(suggestions_student) == 2
    assert suggestions_student[0].student == student
    assert suggestions_student[1].student == student

def test_get_suggestion_by_id(database_session: Session):
    fill_database(database_session)
    suggestion: Suggestion = get_suggestion_by_id(database_session, 1)
    assert suggestion.student_id == 1
    assert suggestion.coach_id == 2
    assert suggestion.suggestion == DecisionEnum.YES
    assert suggestion.argumentation == "Good student"

def test_get_suggestion_by_id_non_existing(database_session: Session):
    with pytest.raises(NoResultFound):
        suggestion: Suggestion = get_suggestion_by_id(database_session, 1)