import pytest
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from src.database.models import Student, User, Edition, Skill
from src.database.enums import DecisionEnum
from src.database.crud.students import get_student_by_id, set_definitive_decision_on_student, delete_student


@pytest.fixture
def database_with_data(database_session: Session):
    """A function to fill the database with fake data that can easly be used when testing"""
    # Editions
    edition: Edition = Edition(year=2022)
    database_session.add(edition)
    database_session.commit()

    # Users
    admin: User = User(name="admin", email="admin@ngmail.com", admin=True)
    coach1: User = User(name="coach1", email="coach1@noutlook.be")
    coach2: User = User(name="coach2", email="coach2@noutlook.be")
    request: User = User(name="request", email="request@ngmail.com")
    database_session.add(admin)
    database_session.add(coach1)
    database_session.add(coach2)
    database_session.add(request)
    database_session.commit()

    # Skill
    skill1: Skill = Skill(name="skill1", description="something about skill1")
    skill2: Skill = Skill(name="skill2", description="something about skill2")
    skill3: Skill = Skill(name="skill3", description="something about skill3")
    skill4: Skill = Skill(name="skill4", description="something about skill4")
    skill5: Skill = Skill(name="skill5", description="something about skill5")
    skill6: Skill = Skill(name="skill6", description="something about skill6")
    database_session.add(skill1)
    database_session.add(skill2)
    database_session.add(skill3)
    database_session.add(skill4)
    database_session.add(skill5)
    database_session.add(skill6)
    database_session.commit()

    # Student
    student01: Student = Student(first_name="Jos", last_name="Vermeulen", preferred_name="Joske",
                                 email_address="josvermeulen@mail.com", phone_number="0487/86.24.45", alumni=True,
                                 wants_to_be_student_coach=True, edition=edition, skills=[skill1, skill3, skill6])
    student30: Student = Student(first_name="Marta", last_name="Marquez", preferred_name="Marta",
                                 email_address="marta.marquez@example.com", phone_number="967-895-285", alumni=True,
                                 wants_to_be_student_coach=False, edition=edition, skills=[skill2, skill4, skill5])

    database_session.add(student01)
    database_session.add(student30)
    database_session.commit()

    return database_session


def test_get_student_by_id(database_with_data: Session):
    """Tests if you get the right student"""
    student: Student = get_student_by_id(database_with_data, 1)
    assert student.first_name == "Jos"
    assert student.last_name == "Vermeulen"
    assert student.student_id == 1
    assert student.email_address == "josvermeulen@mail.com"


def test_no_student(database_with_data: Session):
    """Tests if you get an error for a not existing student"""
    with pytest.raises(NoResultFound):
        get_student_by_id(database_with_data, 5)


def test_definitive_decision_on_student_yes(database_with_data: Session):
    """Tests for definitive decision yes"""
    student: Student = get_student_by_id(database_with_data, 1)
    set_definitive_decision_on_student(
        database_with_data, student, DecisionEnum.YES)
    assert student.decision == DecisionEnum.YES


def test_definitive_decision_on_student_maybe(database_with_data: Session):
    """Tests for definitive decision maybe"""
    student: Student = get_student_by_id(database_with_data, 1)
    set_definitive_decision_on_student(
        database_with_data, student, DecisionEnum.MAYBE)
    assert student.decision == DecisionEnum.MAYBE


def test_definitive_decision_on_student_no(database_with_data: Session):
    """Tests for definitive decision no"""
    student: Student = get_student_by_id(database_with_data, 1)
    set_definitive_decision_on_student(
        database_with_data, student, DecisionEnum.NO)
    assert student.decision == DecisionEnum.NO


def test_delete_student(database_with_data: Session):
    """Tests for deleting a student"""
    student: Student = get_student_by_id(database_with_data, 1)
    delete_student