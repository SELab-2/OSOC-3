import pytest
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from src.database.models import Suggestion, Student, User, Edition, Skill

from src.database.crud.suggestions import ( create_suggestion, get_suggestions_of_student,
                                            get_suggestion_by_id, delete_suggestion, update_suggestion )
from src.database.enums import DecisionEnum

def fill_database(db):
    """A function to fill the database with fake data that can easly be used when testing"""
    # Editions
    edition: Edition = Edition(year=2022)
    db.add(edition)
    db.commit()

    # Users
    admin: User = User(name="admin", email="admin@ngmail.com", admin=True)
    coach1: User = User(name="coach1", email="coach1@noutlook.be")
    coach2: User = User(name="coach2", email="coach2@noutlook.be")
    request: User = User(name="request", email="request@ngmail.com")
    db.add(admin)
    db.add(coach1)
    db.add(coach2)
    db.add(request)
    db.commit()

    # Skill
    skill1: Skill = Skill(name="skill1", description="something about skill1")
    skill2: Skill = Skill(name="skill2", description="something about skill2")
    skill3: Skill = Skill(name="skill3", description="something about skill3")
    skill4: Skill = Skill(name="skill4", description="something about skill4")
    skill5: Skill = Skill(name="skill5", description="something about skill5")
    skill6: Skill = Skill(name="skill6", description="something about skill6")
    db.add(skill1)
    db.add(skill2)
    db.add(skill3)
    db.add(skill4)
    db.add(skill5)
    db.add(skill6)
    db.commit()

    # Student
    student01: Student = Student(first_name="Jos", last_name="Vermeulen", preferred_name="Joske",
                                 email_address="josvermeulen@mail.com", phone_number="0487/86.24.45", alumni=True,
                                 wants_to_be_student_coach=True, edition=edition, skills=[skill1, skill3, skill6])
    student30: Student = Student(first_name="Marta", last_name="Marquez", preferred_name="Marta",
                                 email_address="marta.marquez@example.com", phone_number="967-895-285", alumni=True,
                                 wants_to_be_student_coach=False, edition=edition, skills=[skill2, skill4, skill5])

    db.add(student01)
    db.add(student30)
    db.commit()

    # Suggestion
    suggestion1: Suggestion = Suggestion(
        student=student01, coach=admin, argumentation="Good student", suggestion=DecisionEnum.YES)
    db.add(suggestion1)
    db.commit()


def test_create_suggestion_yes(database_session: Session):
    """Test creat a yes suggestion"""
    fill_database(database_session)

    user: User = database_session.query(
        User).where(User.name == "coach1").first()
    student: Student = database_session.query(Student).where(
        Student.email_address == "marta.marquez@example.com").first()

    new_suggestion = create_suggestion(
        database_session, user.user_id, student.student_id, DecisionEnum.YES, "This is a good student")

    suggestion: Suggestion = database_session.query(Suggestion).where(
        Suggestion.coach == user).where(Suggestion.student_id == student.student_id).one()

    assert new_suggestion == suggestion

    assert suggestion.coach == user
    assert suggestion.student == student
    assert suggestion.suggestion == DecisionEnum.YES
    assert suggestion.argumentation == "This is a good student"


def test_create_suggestion_no(database_session: Session):
    """Test create a no suggestion"""
    fill_database(database_session)

    user: User = database_session.query(
        User).where(User.name == "coach1").first()
    student: Student = database_session.query(Student).where(
        Student.email_address == "marta.marquez@example.com").first()

    new_suggestion = create_suggestion(
        database_session, user.user_id, student.student_id, DecisionEnum.NO, "This is a not good student")

    suggestion: Suggestion = database_session.query(Suggestion).where(
        Suggestion.coach == user).where(Suggestion.student_id == student.student_id).one()

    assert new_suggestion == suggestion

    assert suggestion.coach == user
    assert suggestion.student == student
    assert suggestion.suggestion == DecisionEnum.NO
    assert suggestion.argumentation == "This is a not good student"


def test_create_suggestion_maybe(database_session: Session):
    """Test create a maybe suggestion"""
    fill_database(database_session)

    user: User = database_session.query(
        User).where(User.name == "coach1").first()
    student: Student = database_session.query(Student).where(
        Student.email_address == "marta.marquez@example.com").first()

    new_suggestion = create_suggestion(
        database_session, user.user_id, student.student_id, DecisionEnum.MAYBE, "Idk if it's good student")

    suggestion: Suggestion = database_session.query(Suggestion).where(
        Suggestion.coach == user).where(Suggestion.student_id == student.student_id).one()

    assert new_suggestion == suggestion

    assert suggestion.coach == user
    assert suggestion.student == student
    assert suggestion.suggestion == DecisionEnum.MAYBE
    assert suggestion.argumentation == "Idk if it's good student"


def test_one_coach_two_students(database_session: Session):
    """Test that one coach can write multiple suggestions"""
    fill_database(database_session)

    user: User = database_session.query(
        User).where(User.name == "coach1").one()
    student1: Student = database_session.query(Student).where(
        Student.email_address == "marta.marquez@example.com").one()
    student2: Student = database_session.query(Student).where(
        Student.email_address == "josvermeulen@mail.com").one()

    create_suggestion(database_session, user.user_id,
                      student1.student_id, DecisionEnum.YES, "This is a good student")
    create_suggestion(database_session, user.user_id, student2.student_id,
                      DecisionEnum.NO, "This is a not good student")

    suggestion1: Suggestion = database_session.query(Suggestion).where(
        Suggestion.coach == user).where(Suggestion.student_id == student1.student_id).one()
    assert suggestion1.coach == user
    assert suggestion1.student == student1
    assert suggestion1.suggestion == DecisionEnum.YES
    assert suggestion1.argumentation == "This is a good student"

    suggestion2: Suggestion = database_session.query(Suggestion).where(
        Suggestion.coach == user).where(Suggestion.student_id == student2.student_id).one()
    assert suggestion2.coach == user
    assert suggestion2.student == student2
    assert suggestion2.suggestion == DecisionEnum.NO
    assert suggestion2.argumentation == "This is a not good student"


def test_multiple_suggestions_about_same_student(database_session: Session):
    """Test get multiple suggestions about the same student"""
    fill_database(database_session)

    user: User = database_session.query(
        User).where(User.name == "coach1").first()
    student: Student = database_session.query(Student).where(
        Student.email_address == "marta.marquez@example.com").first()

    create_suggestion(database_session, user.user_id, student.student_id,
                      DecisionEnum.MAYBE, "Idk if it's good student")
    with pytest.raises(IntegrityError):
        create_suggestion(database_session, user.user_id,
                          student.student_id, DecisionEnum.YES, "This is a good student")


def test_get_suggestions_of_student(database_session: Session):
    """Test get all suggestions of a student"""
    fill_database(database_session)

    user1: User = database_session.query(
        User).where(User.name == "coach1").first()
    user2: User = database_session.query(
        User).where(User.name == "coach2").first()
    student: Student = database_session.query(Student).where(
        Student.email_address == "marta.marquez@example.com").first()

    create_suggestion(database_session, user1.user_id, student.student_id,
                      DecisionEnum.MAYBE, "Idk if it's good student")
    create_suggestion(database_session, user2.user_id,
                      student.student_id, DecisionEnum.YES, "This is a good student")
    suggestions_student = get_suggestions_of_student(
        database_session, student.student_id)

    assert len(suggestions_student) == 2
    assert suggestions_student[0].student == student
    assert suggestions_student[1].student == student


def test_get_suggestion_by_id(database_session: Session):
    """Test get suggestion by id"""
    fill_database(database_session)
    suggestion: Suggestion = get_suggestion_by_id(database_session, 1)
    assert suggestion.student_id == 1
    assert suggestion.coach_id == 1
    assert suggestion.suggestion == DecisionEnum.YES
    assert suggestion.argumentation == "Good student"


def test_get_suggestion_by_id_non_existing(database_session: Session):
    """Test you get an error when you search an id that don't exist"""
    with pytest.raises(NoResultFound):
        get_suggestion_by_id(database_session, 1)


def test_delete_suggestion(database_session: Session):
    """Test delete suggestion"""
    fill_database(database_session)

    user: User = database_session.query(
        User).where(User.name == "coach1").first()
    student: Student = database_session.query(Student).where(
        Student.email_address == "marta.marquez@example.com").first()

    create_suggestion(database_session, user.user_id,
                      student.student_id, DecisionEnum.YES, "This is a good student")
    suggestion: Suggestion = database_session.query(Suggestion).where(
        Suggestion.coach == user).where(Suggestion.student_id == student.student_id).one()

    delete_suggestion(database_session, suggestion)

    suggestions: list[Suggestion] = database_session.query(Suggestion).where(
        Suggestion.coach == user).where(Suggestion.student_id == student.student_id).all()
    assert len(suggestions) == 0


def test_update_suggestion(database_session: Session):
    """Test update suggestion"""
    fill_database(database_session)

    user: User = database_session.query(
        User).where(User.name == "coach1").first()
    student: Student = database_session.query(Student).where(
        Student.email_address == "marta.marquez@example.com").first()

    create_suggestion(database_session, user.user_id,
                      student.student_id, DecisionEnum.YES, "This is a good student")
    suggestion: Suggestion = database_session.query(Suggestion).where(
        Suggestion.coach == user).where(Suggestion.student_id == student.student_id).one()

    update_suggestion(database_session, suggestion,
                      DecisionEnum.NO, "Not that good student")

    new_suggestion: Suggestion = database_session.query(Suggestion).where(
        Suggestion.coach == user).where(Suggestion.student_id == student.student_id).one()
    assert new_suggestion.suggestion == DecisionEnum.NO
    assert new_suggestion.argumentation == "Not that good student"
