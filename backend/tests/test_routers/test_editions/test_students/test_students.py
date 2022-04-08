import pytest
from sqlalchemy.orm import Session
from starlette import status
from src.database.enums import DecisionEnum
from src.database.models import Student, User, Edition, Skill, AuthEmail
from src.app.logic.security import get_password_hash

from tests.utils.authorization import AuthClient


@pytest.fixture
def database_with_data(database_session: Session) -> Session:
    """A fixture to fill the database with fake data that can easly be used when testing"""

    # Editions
    edition: Edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
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
                                 email_address="marta.marquez@example.com", phone_number="967-895-285", alumni=False,
                                 wants_to_be_student_coach=False, edition=edition, skills=[skill2, skill4, skill5])

    database_session.add(student01)
    database_session.add(student30)
    database_session.commit()
    return database_session


def test_set_definitive_decision_no_authorization(database_with_data: Session, auth_client: AuthClient):
    """tests"""
    assert auth_client.put(
        "/editions/ed2022/students/2/decision").status_code == status.HTTP_401_UNAUTHORIZED


def test_set_definitive_decision_coach(database_with_data: Session, auth_client: AuthClient):
    """tests"""
    edition: Edition = database_with_data.query(Edition).all()[0]
    auth_client.coach(edition)
    assert auth_client.put(
        "/editions/ed2022/students/2/decision").status_code == status.HTTP_403_FORBIDDEN


def test_set_definitive_decision_on_ghost(database_with_data: Session, auth_client: AuthClient):
    """tests"""
    auth_client.admin()
    assert auth_client.put(
        "/editions/ed2022/students/100/decision").status_code == status.HTTP_404_NOT_FOUND


def test_set_definitive_decision_wrong_body(database_with_data: Session, auth_client: AuthClient):
    """tests"""
    auth_client.admin()
    assert auth_client.put(
        "/editions/ed2022/students/1/decision").status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_set_definitive_decision_yes(database_with_data: Session, auth_client: AuthClient):
    """tests"""
    auth_client.admin()
    assert auth_client.put("/editions/ed2022/students/1/decision",
                           json={"decision": 1}).status_code == status.HTTP_204_NO_CONTENT
    student: Student = database_with_data.query(
        Student).where(Student.student_id == 1).one()
    assert student.decision == DecisionEnum.YES


def test_set_definitive_decision_no(database_with_data: Session, auth_client: AuthClient):
    """tests"""
    auth_client.admin()
    assert auth_client.put("/editions/ed2022/students/1/decision",
                           json={"decision": 3}).status_code == status.HTTP_204_NO_CONTENT
    student: Student = database_with_data.query(
        Student).where(Student.student_id == 1).one()
    assert student.decision == DecisionEnum.NO


def test_set_definitive_decision_maybe(database_with_data: Session, auth_client: AuthClient):
    """tests"""
    auth_client.admin()
    assert auth_client.put("/editions/ed2022/students/1/decision",
                           json={"decision": 2}).status_code == status.HTTP_204_NO_CONTENT
    student: Student = database_with_data.query(
        Student).where(Student.student_id == 1).one()
    assert student.decision == DecisionEnum.MAYBE


def test_delete_student_no_authorization(database_with_data: Session, auth_client: AuthClient):
    """tests"""
    assert auth_client.delete("/editions/ed2022/students/2", headers={
        "Authorization": "auth"}).status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_student_coach(database_with_data: Session, auth_client: AuthClient):
    """tests"""
    edition: Edition = database_with_data.query(Edition).all()[0]
    auth_client.coach(edition)
    assert auth_client.delete(
        "/editions/ed2022/students/2").status_code == status.HTTP_403_FORBIDDEN
    students: Student = database_with_data.query(
        Student).where(Student.student_id == 1).all()
    assert len(students) == 1


def test_delete_ghost(database_with_data: Session, auth_client: AuthClient):
    """tests"""
    auth_client.admin()
    assert auth_client.delete(
        "/editions/ed2022/students/100").status_code == status.HTTP_404_NOT_FOUND
    students: Student = database_with_data.query(
        Student).where(Student.student_id == 1).all()
    assert len(students) == 1


def test_delete(database_with_data: Session, auth_client: AuthClient):
    """tests"""
    auth_client.admin()
    assert auth_client.delete(
        "/editions/ed2022/students/1").status_code == status.HTTP_204_NO_CONTENT
    students: Student = database_with_data.query(
        Student).where(Student.student_id == 1).all()
    assert len(students) == 0


def test_get_student_by_id_no_autorization(database_with_data: Session, auth_client: AuthClient):
    """tests"""
    assert auth_client.get(
        "/editions/ed2022/students/1").status_code == status.HTTP_401_UNAUTHORIZED


def test_get_student_by_id(database_with_data: Session, auth_client: AuthClient):
    """tests"""
    auth_client.admin()
    assert auth_client.get(
        "/editions/ed2022/students/1").status_code == status.HTTP_200_OK


def test_get_students_no_autorization(database_with_data: Session, auth_client: AuthClient):
    """tests"""
    assert auth_client.get(
        "/editions/ed2022/students/").status_code == status.HTTP_401_UNAUTHORIZED


def test_get_all_students(database_with_data: Session, auth_client: AuthClient):
    """tests"""
    edition: Edition = database_with_data.query(Edition).all()[0]
    auth_client.coach(edition)
    response = auth_client.get("/editions/ed2022/students/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["students"]) == 2


def test_get_first_name_students(database_with_data: Session, auth_client: AuthClient):
    """tests"""
    edition: Edition = database_with_data.query(Edition).all()[0]
    auth_client.coach(edition)
    response = auth_client.get("/editions/ed2022/students/?first_name=Jos")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["students"]) == 1


def test_get_last_name_students(database_with_data: Session, auth_client: AuthClient):
    """tests"""
    edition: Edition = database_with_data.query(Edition).all()[0]
    auth_client.coach(edition)
    response = auth_client.get(
        "/editions/ed2022/students/?last_name=Vermeulen")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["students"]) == 1


def test_get_alumni_students(database_with_data: Session, auth_client: AuthClient):
    """tests"""
    edition: Edition = database_with_data.query(Edition).all()[0]
    auth_client.coach(edition)
    response = auth_client.get("/editions/ed2022/students/?alumni=true")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["students"]) == 1


def test_get_student_coach_students(database_with_data: Session, auth_client: AuthClient):
    """tests"""
    edition: Edition = database_with_data.query(Edition).all()[0]
    auth_client.coach(edition)
    response = auth_client.get("/editions/ed2022/students/?student_coach=true")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["students"]) == 1


def test_get_one_skill_students(database_with_data: Session, auth_client: AuthClient):
    """tests"""
    edition: Edition = database_with_data.query(Edition).all()[0]
    auth_client.coach(edition)
    response = auth_client.get("/editions/ed2022/students/?skill_ids=1")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["students"]) == 1
    assert response.json()["students"][0]["firstName"] == "Jos"


def test_get_multiple_skill_students(database_with_data: Session, auth_client: AuthClient):
    """tests"""
    edition: Edition = database_with_data.query(Edition).all()[0]
    auth_client.coach(edition)
    response = auth_client.get(
        "/editions/ed2022/students/?skill_ids=4&skill_ids=5")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["students"]) == 1
    assert response.json()["students"][0]["firstName"] == "Marta"


def test_get_multiple_skill_students_no_students(database_with_data: Session, auth_client: AuthClient):
    """tests"""
    edition: Edition = database_with_data.query(Edition).all()[0]
    auth_client.coach(edition)
    response = auth_client.get(
        "/editions/ed2022/students/?skill_ids=4&skill_ids=6")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["students"]) == 0


def test_get_ghost_skill_students(database_with_data: Session, auth_client: AuthClient):
    """tests"""
    edition: Edition = database_with_data.query(Edition).all()[0]
    auth_client.coach(edition)
    response = auth_client.get("/editions/ed2022/students/?skill_ids=100")
    print(response.json())
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["students"]) == 0


def test_get_one_real_one_ghost_skill_students(database_with_data: Session, auth_client: AuthClient):
    """tests"""
    edition: Edition = database_with_data.query(Edition).all()[0]
    auth_client.coach(edition)
    response = auth_client.get(
        "/editions/ed2022/students/?skill_ids=4&skill_ids=100")
    print(response.json())
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["students"]) == 0
