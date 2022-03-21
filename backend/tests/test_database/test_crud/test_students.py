import pytest
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from src.database.models import Suggestion, Student, User, Edition, Skill
from src.database.crud.students import get_student_by_id

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

def test_get_student_by_id(database_session: Session):
    """Tests if you get the right student"""
    fill_database(database_session)
    student: Student = get_student_by_id(database_session, 1)
    assert student.first_name == "Jos"
    assert student.last_name == "Vermeulen"
    assert student.student_id == 1
    assert student.email_address == "josvermeulen@mail.com"


def test_no_student(database_session: Session):
    """Tests if you get an error for a not existing student"""
    with pytest.raises(NoResultFound):
        get_student_by_id(database_session, 5)
