import datetime
import pytest
from sqlalchemy.orm import Session
from starlette import status
from settings import DB_PAGE_SIZE
from src.database.enums import DecisionEnum, EmailStatusEnum
from src.database.models import Student, Edition, Skill, DecisionEmail

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
    """tests that you have to be logged in"""
    assert auth_client.put(
        "/editions/ed2022/students/2/decision").status_code == status.HTTP_401_UNAUTHORIZED


def test_set_definitive_decision_coach(database_with_data: Session, auth_client: AuthClient):
    """tests that a coach can't set a definitive decision"""
    edition: Edition = database_with_data.query(Edition).all()[0]
    auth_client.coach(edition)
    assert auth_client.put(
        "/editions/ed2022/students/2/decision").status_code == status.HTTP_403_FORBIDDEN


def test_set_definitive_decision_on_ghost(database_with_data: Session, auth_client: AuthClient):
    """tests that you get a 404 if a student don't exicist"""
    auth_client.admin()
    assert auth_client.put(
        "/editions/ed2022/students/100/decision").status_code == status.HTTP_404_NOT_FOUND


def test_set_definitive_decision_wrong_body(database_with_data: Session, auth_client: AuthClient):
    """tests you got a 422 if you give a wrong body"""
    auth_client.admin()
    assert auth_client.put(
        "/editions/ed2022/students/1/decision").status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_set_definitive_decision_yes(database_with_data: Session, auth_client: AuthClient):
    """tests that an admin can set a yes"""
    auth_client.admin()
    assert auth_client.put("/editions/ed2022/students/1/decision",
                           json={"decision": 1}).status_code == status.HTTP_204_NO_CONTENT
    student: Student = database_with_data.query(
        Student).where(Student.student_id == 1).one()
    assert student.decision == DecisionEnum.YES


def test_set_definitive_decision_no(database_with_data: Session, auth_client: AuthClient):
    """tests that an admin can set a no"""
    auth_client.admin()
    assert auth_client.put("/editions/ed2022/students/1/decision",
                           json={"decision": 3}).status_code == status.HTTP_204_NO_CONTENT
    student: Student = database_with_data.query(
        Student).where(Student.student_id == 1).one()
    assert student.decision == DecisionEnum.NO


def test_set_definitive_decision_maybe(database_with_data: Session, auth_client: AuthClient):
    """tests that an admin can set a maybe"""
    auth_client.admin()
    assert auth_client.put("/editions/ed2022/students/1/decision",
                           json={"decision": 2}).status_code == status.HTTP_204_NO_CONTENT
    student: Student = database_with_data.query(
        Student).where(Student.student_id == 1).one()
    assert student.decision == DecisionEnum.MAYBE


def test_delete_student_no_authorization(database_with_data: Session, auth_client: AuthClient):
    """tests that you have to be logged in"""
    assert auth_client.delete(
        "/editions/ed2022/students/2").status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_student_coach(database_with_data: Session, auth_client: AuthClient):
    """tests that a coach can't delete a student"""
    edition: Edition = database_with_data.query(Edition).all()[0]
    auth_client.coach(edition)
    assert auth_client.delete(
        "/editions/ed2022/students/2").status_code == status.HTTP_403_FORBIDDEN
    students: Student = database_with_data.query(
        Student).where(Student.student_id == 1).all()
    assert len(students) == 1


def test_delete_ghost(database_with_data: Session, auth_client: AuthClient):
    """tests that you can't delete a student that don't excist"""
    auth_client.admin()
    assert auth_client.delete(
        "/editions/ed2022/students/100").status_code == status.HTTP_404_NOT_FOUND
    students: Student = database_with_data.query(
        Student).where(Student.student_id == 1).all()
    assert len(students) == 1


def test_delete(database_with_data: Session, auth_client: AuthClient):
    """tests an admin can delete a student"""
    auth_client.admin()
    assert auth_client.delete(
        "/editions/ed2022/students/1").status_code == status.HTTP_204_NO_CONTENT
    students: Student = database_with_data.query(
        Student).where(Student.student_id == 1).all()
    assert len(students) == 0


def test_get_student_by_id_no_autorization(database_with_data: Session, auth_client: AuthClient):
    """tests you have to be logged in to get a student by id"""
    assert auth_client.get(
        "/editions/ed2022/students/1").status_code == status.HTTP_401_UNAUTHORIZED


def test_get_student_by_id(database_with_data: Session, auth_client: AuthClient):
    """tests you can get a student by id"""
    edition: Edition = database_with_data.query(Edition).all()[0]
    auth_client.coach(edition)
    assert auth_client.get(
        "/editions/ed2022/students/1").status_code == status.HTTP_200_OK


def test_get_student_by_id_wrong_edition(database_with_data: Session, auth_client: AuthClient):
    """tests you can get a student by id"""
    edition: Edition = Edition(year=2023, name="ed2023")
    database_with_data.add(edition)
    database_with_data.commit()
    auth_client.coach(edition)
    assert auth_client.get(
        "/editions/ed2023/students/1").status_code == status.HTTP_404_NOT_FOUND


def test_get_students_no_autorization(database_with_data: Session, auth_client: AuthClient):
    """tests you have to be logged in to get all students"""
    assert auth_client.get(
        "/editions/ed2022/students/").status_code == status.HTTP_401_UNAUTHORIZED


def test_get_all_students(database_with_data: Session, auth_client: AuthClient):
    """tests get all students"""
    edition: Edition = database_with_data.query(Edition).all()[0]
    auth_client.coach(edition)
    response = auth_client.get("/editions/ed2022/students/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["students"]) == 2


def test_get_all_students_pagination(database_with_data: Session, auth_client: AuthClient):
    """tests get all students with pagination"""
    edition: Edition = database_with_data.query(Edition).all()[0]
    auth_client.coach(edition)
    for i in range(round(DB_PAGE_SIZE * 1.5)):
        student: Student = Student(first_name=f"Student {i}", last_name="Vermeulen", preferred_name=f"{i}",
                                   email_address=f"student{i}@mail.com", phone_number=f"0487/0{i}.24.45", alumni=True,
                                   wants_to_be_student_coach=True, edition=edition, skills=[])
        database_with_data.add(student)
    database_with_data.commit()
    response = auth_client.get("/editions/ed2022/students/?page=0")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['students']) == DB_PAGE_SIZE
    response = auth_client.get("/editions/ed2022/students/?page=1")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['students']) == max(
        round(DB_PAGE_SIZE * 1.5) - DB_PAGE_SIZE + 2, 0)  # +2 because there were already 2 students in the database


def test_get_first_name_students(database_with_data: Session, auth_client: AuthClient):
    """tests get students based on query paramer first name"""
    edition: Edition = database_with_data.query(Edition).all()[0]
    auth_client.coach(edition)
    response = auth_client.get("/editions/ed2022/students/?first_name=Jos")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["students"]) == 1


def test_get_first_name_student_pagination(database_with_data: Session, auth_client: AuthClient):
    """tests get students based on query paramer first name with pagination"""
    edition: Edition = database_with_data.query(Edition).all()[0]
    auth_client.coach(edition)
    for i in range(round(DB_PAGE_SIZE * 1.5)):
        student: Student = Student(first_name=f"Student {i}", last_name="Vermeulen", preferred_name=f"{i}",
                                   email_address=f"student{i}@mail.com", phone_number=f"0487/0{i}.24.45", alumni=True,
                                   wants_to_be_student_coach=True, edition=edition, skills=[])
        database_with_data.add(student)
    database_with_data.commit()
    response = auth_client.get(
        "/editions/ed2022/students/?first_name=Student&page=0")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["students"]) == DB_PAGE_SIZE
    response = auth_client.get(
        "/editions/ed2022/students/?first_name=Student&page=1")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['students']) == max(
        round(DB_PAGE_SIZE * 1.5) - DB_PAGE_SIZE, 0)


def test_get_last_name_students(database_with_data: Session, auth_client: AuthClient):
    """tests get students based on query paramer last name"""
    edition: Edition = database_with_data.query(Edition).all()[0]
    auth_client.coach(edition)
    response = auth_client.get(
        "/editions/ed2022/students/?last_name=Vermeulen")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["students"]) == 1


def test_get_last_name_students_pagination(database_with_data: Session, auth_client: AuthClient):
    """tests get students based on query paramer last name with pagination"""
    edition: Edition = database_with_data.query(Edition).all()[0]
    auth_client.coach(edition)
    for i in range(round(DB_PAGE_SIZE * 1.5)):
        student: Student = Student(first_name="Jos", last_name=f"Student {i}", preferred_name=f"{i}",
                                   email_address=f"student{i}@mail.com", phone_number=f"0487/0{i}.24.45", alumni=True,
                                   wants_to_be_student_coach=True, edition=edition, skills=[])
        database_with_data.add(student)
    database_with_data.commit()
    response = auth_client.get(
        "/editions/ed2022/students/?last_name=Student&page=0")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["students"]) == DB_PAGE_SIZE
    response = auth_client.get(
        "/editions/ed2022/students/?last_name=Student&page=1")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['students']) == max(
        round(DB_PAGE_SIZE * 1.5) - DB_PAGE_SIZE, 0)


def test_get_alumni_students(database_with_data: Session, auth_client: AuthClient):
    """tests get students based on query paramer alumni"""
    edition: Edition = database_with_data.query(Edition).all()[0]
    auth_client.coach(edition)
    response = auth_client.get("/editions/ed2022/students/?alumni=true")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["students"]) == 1


def test_get_alumni_students_pagination(database_with_data: Session, auth_client: AuthClient):
    """tests get students based on query paramer alumni with pagination"""
    edition: Edition = database_with_data.query(Edition).all()[0]
    auth_client.coach(edition)
    for i in range(round(DB_PAGE_SIZE * 1.5)):
        student: Student = Student(first_name="Jos", last_name=f"Student {i}", preferred_name=f"{i}",
                                   email_address=f"student{i}@mail.com", phone_number=f"0487/0{i}.24.45", alumni=True,
                                   wants_to_be_student_coach=True, edition=edition, skills=[])
        database_with_data.add(student)
    database_with_data.commit()
    response = auth_client.get(
        "/editions/ed2022/students/?alumni=true&page=0")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["students"]) == DB_PAGE_SIZE
    response = auth_client.get(
        "/editions/ed2022/students/?alumni=true&page=1")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['students']) == max(
        round(DB_PAGE_SIZE * 1.5) - DB_PAGE_SIZE + 1, 0)  # +1 because there is already is one


def test_get_student_coach_students(database_with_data: Session, auth_client: AuthClient):
    """tests get students based on query paramer student coach"""
    edition: Edition = database_with_data.query(Edition).all()[0]
    auth_client.coach(edition)
    response = auth_client.get("/editions/ed2022/students/?student_coach=true")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["students"]) == 1


def test_get_student_coach_students_pagination(database_with_data: Session, auth_client: AuthClient):
    """tests get students based on query paramer student coach with pagination"""
    edition: Edition = database_with_data.query(Edition).all()[0]
    auth_client.coach(edition)
    for i in range(round(DB_PAGE_SIZE * 1.5)):
        student: Student = Student(first_name="Jos", last_name=f"Student {i}", preferred_name=f"{i}",
                                   email_address=f"student{i}@mail.com", phone_number=f"0487/0{i}.24.45", alumni=True,
                                   wants_to_be_student_coach=True, edition=edition, skills=[])
        database_with_data.add(student)
    database_with_data.commit()
    response = auth_client.get(
        "/editions/ed2022/students/?student_coach=true&page=0")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["students"]) == DB_PAGE_SIZE
    response = auth_client.get(
        "/editions/ed2022/students/?student_coach=true&page=1")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['students']) == max(
        round(DB_PAGE_SIZE * 1.5) - DB_PAGE_SIZE + 1, 0)  # +1 because there is already is one


def test_get_one_skill_students(database_with_data: Session, auth_client: AuthClient):
    """tests get students based on query paramer one skill"""
    edition: Edition = database_with_data.query(Edition).all()[0]
    auth_client.coach(edition)
    response = auth_client.get("/editions/ed2022/students/?skill_ids=1")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["students"]) == 1
    assert response.json()["students"][0]["firstName"] == "Jos"


def test_get_multiple_skill_students(database_with_data: Session, auth_client: AuthClient):
    """tests get students based on query paramer multiple skills"""
    edition: Edition = database_with_data.query(Edition).all()[0]
    auth_client.coach(edition)
    response = auth_client.get(
        "/editions/ed2022/students/?skill_ids=4&skill_ids=5")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["students"]) == 1
    assert response.json()["students"][0]["firstName"] == "Marta"


def test_get_multiple_skill_students_no_students(database_with_data: Session, auth_client: AuthClient):
    """tests get students based on query paramer multiple skills, but that student don't excist"""
    edition: Edition = database_with_data.query(Edition).all()[0]
    auth_client.coach(edition)
    response = auth_client.get(
        "/editions/ed2022/students/?skill_ids=4&skill_ids=6")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["students"]) == 0


def test_get_ghost_skill_students(database_with_data: Session, auth_client: AuthClient):
    """tests get students based on query paramer one skill that don't excist"""
    edition: Edition = database_with_data.query(Edition).all()[0]
    auth_client.coach(edition)
    response = auth_client.get("/editions/ed2022/students/?skill_ids=100")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["students"]) == 0


def test_get_one_real_one_ghost_skill_students(database_with_data: Session, auth_client: AuthClient):
    """tests get students based on query paramer one skill that excist and one that don't excist"""
    edition: Edition = database_with_data.query(Edition).all()[0]
    auth_client.coach(edition)
    response = auth_client.get(
        "/editions/ed2022/students/?skill_ids=4&skill_ids=100")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["students"]) == 0


def test_get_emails_student_no_authorization(database_with_data: Session, auth_client: AuthClient):
    """tests that you can't get the mails of a student when you aren't logged in"""
    response = auth_client.get("/editions/ed2022/students/1/emails")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_emails_student_coach(database_with_data: Session, auth_client: AuthClient):
    """tests that a coach can't get the mails of a student"""
    edition: Edition = database_with_data.query(Edition).all()[0]
    auth_client.coach(edition)
    response = auth_client.get("/editions/ed2022/students/1/emails")
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_emails_student_admin(database_with_data: Session, auth_client: AuthClient):
    """tests that an admin can get the mails of a student"""
    auth_client.admin()
    auth_client.post("/editions/ed2022/students/emails",
                     json={"students_id": [1], "email_status": 1})
    response = auth_client.get("/editions/ed2022/students/1/emails")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["emails"]) == 1
    assert response.json()["student"]["studentId"] == 1
    response = auth_client.get("/editions/ed2022/students/2/emails")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["emails"]) == 0
    assert response.json()["student"]["studentId"] == 2


def test_post_email_no_authorization(database_with_data: Session, auth_client: AuthClient):
    """tests user need to be loged in"""
    response = auth_client.post("/editions/ed2022/students/emails")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_post_email_coach(database_with_data: Session, auth_client: AuthClient):
    """tests user can't be a coach"""
    edition: Edition = database_with_data.query(Edition).all()[0]
    auth_client.coach(edition)
    response = auth_client.post("/editions/ed2022/students/emails")
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_post_email_applied(database_with_data: Session, auth_client: AuthClient):
    """test create email applied"""
    auth_client.admin()
    response = auth_client.post("/editions/ed2022/students/emails",
                                json={"students_id": [2], "email_status": 0})
    assert response.status_code == status.HTTP_201_CREATED
    assert EmailStatusEnum(
        response.json()["studentEmails"][0]["emails"][0]["decision"]) == EmailStatusEnum.APPLIED


def test_post_email_awaiting_project(database_with_data: Session, auth_client: AuthClient):
    """test create email awaiting project"""
    auth_client.admin()
    response = auth_client.post("/editions/ed2022/students/emails",
                                json={"students_id": [2], "email_status": 1})
    assert response.status_code == status.HTTP_201_CREATED
    assert EmailStatusEnum(
        response.json()["studentEmails"][0]["emails"][0]["decision"]) == EmailStatusEnum.AWAITING_PROJECT


def test_post_email_approved(database_with_data: Session, auth_client: AuthClient):
    """test create email applied"""
    auth_client.admin()
    response = auth_client.post("/editions/ed2022/students/emails",
                                json={"students_id": [2], "email_status": 2})
    assert response.status_code == status.HTTP_201_CREATED
    assert EmailStatusEnum(
        response.json()["studentEmails"][0]["emails"][0]["decision"]) == EmailStatusEnum.APPROVED


def test_post_email_contract_confirmed(database_with_data: Session, auth_client: AuthClient):
    """test create email contract confirmed"""
    auth_client.admin()
    response = auth_client.post("/editions/ed2022/students/emails",
                                json={"students_id": [2], "email_status": 3})
    assert response.status_code == status.HTTP_201_CREATED
    assert EmailStatusEnum(
        response.json()["studentEmails"][0]["emails"][0]["decision"]) == EmailStatusEnum.CONTRACT_CONFIRMED


def test_post_email_contract_declined(database_with_data: Session, auth_client: AuthClient):
    """test create email contract declined"""
    auth_client.admin()
    response = auth_client.post("/editions/ed2022/students/emails",
                                json={"students_id": [2], "email_status": 4})
    assert response.status_code == status.HTTP_201_CREATED
    assert EmailStatusEnum(
        response.json()["studentEmails"][0]["emails"][0]["decision"]) == EmailStatusEnum.CONTRACT_DECLINED


def test_post_email_rejected(database_with_data: Session, auth_client: AuthClient):
    """test create email rejected"""
    auth_client.admin()
    response = auth_client.post("/editions/ed2022/students/emails",
                                json={"students_id": [2], "email_status": 5})
    assert response.status_code == status.HTTP_201_CREATED
    print(response.json())
    assert EmailStatusEnum(
        response.json()["studentEmails"][0]["emails"][0]["decision"]) == EmailStatusEnum.REJECTED


def test_creat_email_for_ghost(database_with_data: Session, auth_client: AuthClient):
    """test create email for student that don't exist"""
    auth_client.admin()
    response = auth_client.post("/editions/ed2022/students/emails",
                                json={"students_id": [100], "email_status": 5})
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_creat_email_student_in_other_edition(database_with_data: Session, auth_client: AuthClient):
    """test creat an email for a student not in this edition"""
    edition: Edition = Edition(year=2023, name="ed2023")
    database_with_data.add(edition)
    student: Student = Student(first_name="Mehmet", last_name="Dizdar", preferred_name="Mehmet",
                               email_address="mehmet.dizdar@example.com", phone_number="(787)-938-6216", alumni=True,
                               wants_to_be_student_coach=False, edition=edition, skills=[])
    database_with_data.add(student)
    database_with_data.commit()
    auth_client.admin()
    response = auth_client.post("/editions/ed2022/students/emails",
                                json={"students_id": [3], "email_status": 5})
    print(response.json())
    assert response.status_code == status.HTTP_201_CREATED
    assert len(response.json()["studentEmails"]) == 0


def test_get_emails_no_authorization(database_with_data: Session, auth_client: AuthClient):
    """test get emails not loged in"""
    response = auth_client.get("/editions/ed2022/students/emails")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_emails_coach(database_with_data: Session, auth_client: AuthClient):
    """test get emails logged in as coach"""
    edition: Edition = database_with_data.query(Edition).all()[0]
    auth_client.coach(edition)
    response = auth_client.post("/editions/ed2022/students/emails")
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_emails(database_with_data: Session, auth_client: AuthClient):
    """test get emails"""
    auth_client.admin()
    response = auth_client.post("/editions/ed2022/students/emails",
                                json={"students_id": [1], "email_status": 3})
    auth_client.post("/editions/ed2022/students/emails",
                     json={"students_id": [2], "email_status": 5})
    response = auth_client.get("/editions/ed2022/students/emails")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["studentEmails"]) == 2
    assert response.json()["studentEmails"][0]["student"]["studentId"] == 1
    assert response.json()["studentEmails"][0]["emails"][0]["decision"] == 3
    assert response.json()["studentEmails"][1]["student"]["studentId"] == 2
    assert response.json()["studentEmails"][1]["emails"][0]["decision"] == 5


def test_emails_filter_first_name(database_with_data: Session, auth_client: AuthClient):
    """test get emails with filter first name"""
    auth_client.admin()
    auth_client.post("/editions/ed2022/students/emails",
                     json={"students_id": [1], "email_status": 1})
    response = auth_client.get(
        "/editions/ed2022/students/emails/?first_name=Jos")
    assert len(response.json()["studentEmails"]) == 1
    assert response.json()["studentEmails"][0]["student"]["firstName"] == "Jos"


def test_emails_filter_last_name(database_with_data: Session, auth_client: AuthClient):
    """test get emails with filter last name"""
    auth_client.admin()
    auth_client.post("/editions/ed2022/students/emails",
                     json={"students_id": [1], "email_status": 1})
    response = auth_client.get(
        "/editions/ed2022/students/emails/?last_name=Vermeulen")
    assert len(response.json()["studentEmails"]) == 1
    assert response.json()[
        "studentEmails"][0]["student"]["lastName"] == "Vermeulen"


def test_emails_filter_emailstatus(database_with_data: Session, auth_client: AuthClient):
    """test to get all email status, and you only filter on the email send"""
    auth_client.admin()
    for i in range(0, 6):
        auth_client.post("/editions/ed2022/students/emails",
                         json={"students_id": [2], "email_status": i})
        response = auth_client.get(
            f"/editions/ed2022/students/emails/?email_status={i}")
        print(response.json())
        assert len(response.json()["studentEmails"]) == 1
        if i > 0:
            response = auth_client.get(
                f"/editions/ed2022/students/emails/?email_status={i-1}")
            assert len(response.json()["studentEmails"]) == 0


def test_emails_filter_emailstatus_multiple_status(database_with_data: Session, auth_client: AuthClient):
    """test to get all email status with multiple status"""
    auth_client.admin()
    auth_client.post("/editions/ed2022/students/emails",
                     json={"students_id": [2], "email_status": 1})
    auth_client.post("/editions/ed2022/students/emails",
                     json={"students_id": [1], "email_status": 3})
    response = auth_client.get(
        "/editions/ed2022/students/emails/?email_status=3&email_status=1")
    assert len(response.json()["studentEmails"]) == 2
    assert response.json()["studentEmails"][0]["student"]["studentId"] == 1
    assert response.json()["studentEmails"][1]["student"]["studentId"] == 2
