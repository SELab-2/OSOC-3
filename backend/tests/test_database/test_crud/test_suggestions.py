import pytest
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.database.models import Suggestion, Student, User

from src.database.crud.suggestions import create_suggestion, get_suggestions_of_student
from tests.fill_database import fill_database
from src.database.enums import DecisionEnum

def test_create_suggestion_yes(database_session: Session):
    fill_database(database_session)

    user: User = database_session.query(User).where(User.name == "coach1").first()
    student: Student = database_session.query(Student).where(Student.email_address == "marta.marquez@example.com").first()
    
    create_suggestion(database_session, user.user_id, student.student_id, DecisionEnum.YES, "This is a good student")

    suggestion: Suggestion = database_session.query(Suggestion).where(Suggestion.coach == user and Suggestion.student == student).first()

    assert suggestion.coach == user
    assert suggestion.student == student
    assert suggestion.suggestion == DecisionEnum.YES
    assert suggestion.argumentation == "This is a good student"

def test_create_suggestion_no(database_session: Session):
    fill_database(database_session)

    user: User = database_session.query(User).where(User.name == "coach1").first()
    student: Student = database_session.query(Student).where(Student.email_address == "marta.marquez@example.com").first()
    
    create_suggestion(database_session, user.user_id, student.student_id, DecisionEnum.NO, "This is a not good student")

    suggestion: Suggestion = database_session.query(Suggestion).where(Suggestion.coach == user and Suggestion.student == student).first()

    assert suggestion.coach == user
    assert suggestion.student == student
    assert suggestion.suggestion == DecisionEnum.NO
    assert suggestion.argumentation == "This is a not good student"

def test_create_suggestion_maybe(database_session: Session):
    fill_database(database_session)

    user: User = database_session.query(User).where(User.name == "coach1").first()
    student: Student = database_session.query(Student).where(Student.email_address == "marta.marquez@example.com").first()
    
    create_suggestion(database_session, user.user_id, student.student_id, DecisionEnum.MAYBE, "Idk if it's good student")

    suggestion: Suggestion = database_session.query(Suggestion).where(Suggestion.coach == user and Suggestion.student == student).first()

    assert suggestion.coach == user
    assert suggestion.student == student
    assert suggestion.suggestion == DecisionEnum.MAYBE
    assert suggestion.argumentation == "Idk if it's good student"

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
