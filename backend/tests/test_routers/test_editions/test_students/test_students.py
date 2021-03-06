import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from settings import DB_PAGE_SIZE
from src.database.enums import DecisionEnum, EmailStatusEnum
from src.database.models import Student, Edition, Skill, DecisionEmail

from tests.utils.authorization import AuthClient


@pytest.fixture
async def database_with_data(database_session: AsyncSession) -> AsyncSession:
    """A fixture to fill the database with fake data that can easly be used when testing"""

    # Editions
    edition: Edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)

    # Skill
    skill1: Skill = Skill(name="skill1")
    skill2: Skill = Skill(name="skill2")
    skill3: Skill = Skill(name="skill3")
    skill4: Skill = Skill(name="skill4")
    skill5: Skill = Skill(name="skill5")
    skill6: Skill = Skill(name="skill6")
    database_session.add(skill1)
    database_session.add(skill2)
    database_session.add(skill3)
    database_session.add(skill4)
    database_session.add(skill5)
    database_session.add(skill6)

    # Student
    student01: Student = Student(first_name="Jos", last_name="Vermeulen", preferred_name="Joske",
                                 email_address="josvermeulen@mail.com", phone_number="0487/86.24.45", alumni=True,
                                 wants_to_be_student_coach=True, edition=edition, skills=[skill1, skill3, skill6])
    student30: Student = Student(first_name="Marta", last_name="Marquez", preferred_name="Marta",
                                 email_address="marta.marquez@example.com", phone_number="967-895-285", alumni=False,
                                 decision=DecisionEnum.YES, wants_to_be_student_coach=False, edition=edition,
                                 skills=[skill2, skill4, skill5])

    database_session.add(student01)
    database_session.add(student30)
    await database_session.commit()

    return database_session


@pytest.fixture
async def current_edition(database_with_data: AsyncSession) -> Edition:
    """fixture to get the latest edition"""
    return (await database_with_data.execute(select(Edition))).scalars().all()[-1]


async def test_set_definitive_decision_no_authorization(database_with_data: AsyncSession, auth_client: AuthClient):
    """tests that you have to be logged in"""
    async with auth_client:
        response = await auth_client.put("/editions/ed2022/students/2/decision")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_set_definitive_decision_coach(database_with_data: AsyncSession,
                                             auth_client: AuthClient, current_edition: Edition):
    """tests that a coach can't set a definitive decision"""
    await auth_client.coach(current_edition)
    async with auth_client:
        response = await auth_client.put("/editions/ed2022/students/2/decision")
        assert response.status_code == status.HTTP_403_FORBIDDEN


async def test_set_definitive_decision_on_ghost(database_with_data: AsyncSession, auth_client: AuthClient):
    """tests that you get a 404 if a student don't exicist"""
    await auth_client.admin()
    async with auth_client:
        response = await auth_client.put("/editions/ed2022/students/100/decision")
        assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_set_definitive_decision_wrong_body(database_with_data: AsyncSession, auth_client: AuthClient):
    """tests you got a 422 if you give a wrong body"""
    await auth_client.admin()
    async with auth_client:
        response = await auth_client.put("/editions/ed2022/students/1/decision")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_set_definitive_decision_yes(database_with_data: AsyncSession, auth_client: AuthClient):
    """tests that an admin can set a yes"""
    await auth_client.admin()
    async with auth_client:
        response = await auth_client.put("/editions/ed2022/students/1/decision", json={"decision": 1})
        assert response.status_code == status.HTTP_204_NO_CONTENT
        query = select(Student).where(Student.student_id == 1)
        result = await database_with_data.execute(query)
        student: Student = result.unique().scalars().one()
        assert student.decision == DecisionEnum.YES


async def test_set_definitive_decision_no(database_with_data: AsyncSession, auth_client: AuthClient):
    """tests that an admin can set a no"""
    await auth_client.admin()
    async with auth_client:
        response = await auth_client.put("/editions/ed2022/students/1/decision", json={"decision": 3})
        assert response.status_code == status.HTTP_204_NO_CONTENT
        query = select(Student).where(Student.student_id == 1)
        result = await database_with_data.execute(query)
        student: Student = result.unique().scalars().one()
        assert student.decision == DecisionEnum.NO


async def test_set_definitive_decision_maybe(database_with_data: AsyncSession, auth_client: AuthClient):
    """tests that an admin can set a maybe"""
    await auth_client.admin()
    async with auth_client:
        response = await auth_client.put("/editions/ed2022/students/1/decision", json={"decision": 2})
        assert response.status_code == status.HTTP_204_NO_CONTENT
        query = select(Student).where(Student.student_id == 1)
        result = await database_with_data.execute(query)
        student: Student = result.unique().scalars().one()
        assert student.decision == DecisionEnum.MAYBE


async def test_delete_student_no_authorization(database_with_data: AsyncSession, auth_client: AuthClient):
    """tests that you have to be logged in"""
    async with auth_client:
        response = await auth_client.delete("/editions/ed2022/students/2")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_delete_student_coach(database_with_data: AsyncSession, auth_client: AuthClient,
                                    current_edition: Edition):
    """tests that a coach can't delete a student"""
    await auth_client.coach(current_edition)
    async with auth_client:
        response = await auth_client.delete("/editions/ed2022/students/2")
        assert response.status_code == status.HTTP_403_FORBIDDEN
        query = select(Student).where(Student.student_id == 1)
        result = await database_with_data.execute(query)
        students: list[Student] = result.unique().scalars().all()
        assert len(students) == 1


async def test_delete_ghost(database_with_data: AsyncSession, auth_client: AuthClient):
    """tests that you can't delete a student that don't excist"""
    await auth_client.admin()
    async with auth_client:
        response = await auth_client.delete("/editions/ed2022/students/100")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        query = select(Student).where(Student.student_id == 1)
        result = await database_with_data.execute(query)
        students: list[Student] = result.unique().scalars().all()
        assert len(students) == 1


async def test_delete(database_with_data: AsyncSession, auth_client: AuthClient):
    """tests an admin can delete a student"""
    await auth_client.admin()
    async with auth_client:
        response = await auth_client.delete("/editions/ed2022/students/1")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        query = select(Student).where(Student.student_id == 1)
        result = await database_with_data.execute(query)
        students: list[Student] = result.unique().scalars().all()
        assert len(students) == 0


async def test_get_student_by_id_no_autorization(database_with_data: AsyncSession, auth_client: AuthClient):
    """tests you have to be logged in to get a student by id"""
    async with auth_client:
        response = await auth_client.get("/editions/ed2022/students/1")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_get_student_by_id(database_with_data: AsyncSession, auth_client: AuthClient,
                                 current_edition: Edition):
    """tests you can get a student by id"""
    await auth_client.coach(current_edition)
    async with auth_client:
        response = await auth_client.get("/editions/ed2022/students/1")
        assert response.status_code == status.HTTP_200_OK


async def test_get_student_by_id_wrong_edition(database_with_data: AsyncSession, auth_client: AuthClient,
                                               current_edition: Edition):
    """tests you can get a student by id"""
    edition: Edition = Edition(year=2023, name="ed2023")
    database_with_data.add(edition)
    await database_with_data.commit()
    await auth_client.coach(edition)
    async with auth_client:
        response = await auth_client.get("/editions/ed2023/students/1")
        assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_get_students_no_autorization(database_with_data: AsyncSession, auth_client: AuthClient):
    """tests you have to be logged in to get all students"""
    async with auth_client:
        assert (await auth_client.get(
            "/editions/ed2022/students/", follow_redirects=True)).status_code == status.HTTP_401_UNAUTHORIZED


async def test_get_all_students(database_with_data: AsyncSession, auth_client: AuthClient,
                                current_edition: Edition):
    """tests get all students"""
    await auth_client.coach(current_edition)
    async with auth_client:
        response = await auth_client.get("/editions/ed2022/students/", follow_redirects=True)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()["students"]) == 2


async def test_get_all_students_pagination(database_with_data: AsyncSession, auth_client: AuthClient):
    """tests get all students with pagination"""
    edition: Edition = (await database_with_data.execute(select(Edition))).scalars().all()[0]
    await auth_client.coach(edition)
    for i in range(round(DB_PAGE_SIZE * 1.5)):
        student: Student = Student(first_name=f"Student {i}", last_name="Vermeulen", preferred_name=f"{i}",
                                   email_address=f"student{i}@mail.com", phone_number=f"0487/0{i}.24.45", alumni=True,
                                   wants_to_be_student_coach=True, edition=edition, skills=[])
        database_with_data.add(student)
    await database_with_data.commit()
    async with auth_client:
        response = await auth_client.get("/editions/ed2022/students?page=0", follow_redirects=True)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()['students']) == DB_PAGE_SIZE
        response = await auth_client.get("/editions/ed2022/students?page=1", follow_redirects=True)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()['students']) == max(
            round(DB_PAGE_SIZE * 1.5) - DB_PAGE_SIZE + 2, 0)  # +2 because there were already 2 students in the database


async def test_get_first_name_students(database_with_data: AsyncSession, auth_client: AuthClient):
    """tests get students based on query paramer first name"""
    edition: Edition = (await database_with_data.execute(select(Edition))).scalars().all()[0]
    await auth_client.coach(edition)
    async with auth_client:
        response = await auth_client.get("/editions/ed2022/students?name=Jos", follow_redirects=True)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["students"]) == 1


async def test_get_first_name_student_pagination(database_with_data: AsyncSession, auth_client: AuthClient):
    """tests get students based on query paramer first name with pagination"""
    edition: Edition = (await database_with_data.execute(select(Edition))).scalars().all()[0]
    await auth_client.coach(edition)
    for i in range(round(DB_PAGE_SIZE * 1.5)):
        student: Student = Student(first_name=f"Student {i}", last_name="Vermeulen", preferred_name=f"{i}",
                                   email_address=f"student{i}@mail.com", phone_number=f"0487/0{i}.24.45", alumni=True,
                                   wants_to_be_student_coach=True, edition=edition, skills=[])
        database_with_data.add(student)
    await database_with_data.commit()
    async with auth_client:
        response = await auth_client.get(
            "/editions/ed2022/students?name=Student&page=0", follow_redirects=True)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()["students"]) == DB_PAGE_SIZE
        response = await auth_client.get(
            "/editions/ed2022/students?name=Student&page=1", follow_redirects=True)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()['students']) == max(
            round(DB_PAGE_SIZE * 1.5) - DB_PAGE_SIZE, 0)


async def test_get_last_name_students(database_with_data: AsyncSession, auth_client: AuthClient):
    """tests get students based on query paramer last name"""
    edition: Edition = (await database_with_data.execute(select(Edition))).scalars().all()[0]
    await auth_client.coach(edition)
    async with auth_client:
        response = await auth_client.get(
            "/editions/ed2022/students?name=Vermeulen", follow_redirects=True)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["students"]) == 1


async def test_get_last_name_students_pagination(database_with_data: AsyncSession, auth_client: AuthClient):
    """tests get students based on query paramer last name with pagination"""
    edition: Edition = (await database_with_data.execute(select(Edition))).scalars().all()[0]
    await auth_client.coach(edition)
    for i in range(round(DB_PAGE_SIZE * 1.5)):
        student: Student = Student(first_name="Jos", last_name=f"Student {i}", preferred_name=f"{i}",
                                   email_address=f"student{i}@mail.com", phone_number=f"0487/0{i}.24.45", alumni=True,
                                   wants_to_be_student_coach=True, edition=edition, skills=[])
        database_with_data.add(student)
    await database_with_data.commit()
    async with auth_client:
        response = await auth_client.get(
            "/editions/ed2022/students?name=Student&page=0", follow_redirects=True)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()["students"]) == DB_PAGE_SIZE
        response = await auth_client.get(
            "/editions/ed2022/students?name=Student&page=1", follow_redirects=True)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()['students']) == max(
            round(DB_PAGE_SIZE * 1.5) - DB_PAGE_SIZE, 0)


async def test_get_between_first_and_last_name_students(database_with_data: AsyncSession, auth_client: AuthClient):
    """tests get students based on query paramer first- and last name"""
    edition: Edition = (await database_with_data.execute(select(Edition))).scalars().all()[0]
    await auth_client.coach(edition)
    async with auth_client:
        response = await auth_client.get(
            "/editions/ed2022/students?name=os V", follow_redirects=True)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()["students"]) == 1


async def test_get_alumni_students(database_with_data: AsyncSession, auth_client: AuthClient):
    """tests get students based on query paramer alumni"""
    edition: Edition = (await database_with_data.execute(select(Edition))).scalars().all()[0]
    await auth_client.coach(edition)
    async with auth_client:
        response = await auth_client.get("/editions/ed2022/students?alumni=true", follow_redirects=True)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()["students"]) == 1


async def test_get_alumni_students_pagination(database_with_data: AsyncSession, auth_client: AuthClient):
    """tests get students based on query paramer alumni with pagination"""
    edition: Edition = (await database_with_data.execute(select(Edition))).scalars().all()[0]
    await auth_client.coach(edition)
    for i in range(round(DB_PAGE_SIZE * 1.5)):
        student: Student = Student(first_name="Jos", last_name=f"Student {i}", preferred_name=f"{i}",
                                   email_address=f"student{i}@mail.com", phone_number=f"0487/0{i}.24.45", alumni=True,
                                   wants_to_be_student_coach=True, edition=edition, skills=[])
        database_with_data.add(student)
    await database_with_data.commit()
    async with auth_client:
        response = await auth_client.get(
            "/editions/ed2022/students?alumni=true&page=0", follow_redirects=True)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()["students"]) == DB_PAGE_SIZE
        response = await auth_client.get(
            "/editions/ed2022/students?alumni=true&page=1", follow_redirects=True)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()['students']) == max(
            round(DB_PAGE_SIZE * 1.5) - DB_PAGE_SIZE + 1, 0)  # +1 because there is already is one


async def test_get_student_coach_students(database_with_data: AsyncSession, auth_client: AuthClient):
    """tests get students based on query paramer student coach"""
    edition: Edition = (await database_with_data.execute(select(Edition))).scalars().all()[0]
    await auth_client.coach(edition)
    async with auth_client:
        response = await auth_client.get("/editions/ed2022/students?student_coach=true", follow_redirects=True)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["students"]) == 1


async def test_get_student_coach_students_pagination(database_with_data: AsyncSession, auth_client: AuthClient):
    """tests get students based on query paramer student coach with pagination"""
    edition: Edition = (await database_with_data.execute(select(Edition))).scalars().all()[0]
    await auth_client.coach(edition)
    for i in range(round(DB_PAGE_SIZE * 1.5)):
        student: Student = Student(first_name="Jos", last_name=f"Student {i}", preferred_name=f"{i}",
                                   email_address=f"student{i}@mail.com", phone_number=f"0487/0{i}.24.45", alumni=True,
                                   wants_to_be_student_coach=True, edition=edition, skills=[])
        database_with_data.add(student)
    await database_with_data.commit()
    async with auth_client:
        response = await auth_client.get(
            "/editions/ed2022/students?student_coach=true&page=0", follow_redirects=True)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()["students"]) == DB_PAGE_SIZE
        response = await auth_client.get(
            "/editions/ed2022/students?student_coach=true&page=1", follow_redirects=True)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()['students']) == max(
            round(DB_PAGE_SIZE * 1.5) - DB_PAGE_SIZE + 1, 0)  # +1 because there is already is one


async def test_get_one_skill_students(database_with_data: AsyncSession, auth_client: AuthClient):
    """tests get students based on query paramer one skill"""
    edition: Edition = (await database_with_data.execute(select(Edition))).scalars().all()[0]
    await auth_client.coach(edition)
    async with auth_client:
        response = await auth_client.get("/editions/ed2022/students?skill_ids=1", follow_redirects=True)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["students"]) == 1
    assert response.json()["students"][0]["firstName"] == "Jos"


async def test_get_multiple_skill_students(database_with_data: AsyncSession, auth_client: AuthClient):
    """tests get students based on query paramer multiple skills"""
    edition: Edition = (await database_with_data.execute(select(Edition))).scalars().all()[0]
    await auth_client.coach(edition)
    async with auth_client:
        response = await auth_client.get(
            "/editions/ed2022/students?skill_ids=4&skill_ids=5", follow_redirects=True)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["students"]) == 1
    assert response.json()["students"][0]["firstName"] == "Marta"


async def test_get_multiple_skill_students_no_students(database_with_data: AsyncSession, auth_client: AuthClient):
    """tests get students based on query paramer multiple skills, but that student don't excist"""
    edition: Edition = (await database_with_data.execute(select(Edition))).scalars().all()[0]
    await auth_client.coach(edition)
    async with auth_client:
        response = await auth_client.get(
            "/editions/ed2022/students?skill_ids=4&skill_ids=6", follow_redirects=True)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["students"]) == 0


async def test_get_ghost_skill_students(database_with_data: AsyncSession, auth_client: AuthClient):
    """tests get students based on query paramer one skill that don't excist"""
    edition: Edition = (await database_with_data.execute(select(Edition))).scalars().all()[0]
    await auth_client.coach(edition)
    async with auth_client:
        response = await auth_client.get("/editions/ed2022/students?skill_ids=100", follow_redirects=True)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["students"]) == 0


async def test_get_one_real_one_ghost_skill_students(database_with_data: AsyncSession, auth_client: AuthClient):
    """tests get students based on query paramer one skill that excist and one that don't excist"""
    edition: Edition = (await database_with_data.execute(select(Edition))).scalars().all()[0]
    await auth_client.coach(edition)
    async with auth_client:
        response = await auth_client.get(
            "/editions/ed2022/students?skill_ids=4&skill_ids=100", follow_redirects=True)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["students"]) == 0


async def test_get_students_filter_decisions_one(database_with_data: AsyncSession, auth_client: AuthClient):
    """tests get students based on query parameter decisions"""
    edition: Edition = (await database_with_data.execute(select(Edition))).scalars().all()[0]
    await auth_client.coach(edition)
    async with auth_client:
        response = await auth_client.get(
            "/editions/ed2022/students?decisions=0", follow_redirects=True)
        print(response.content)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["students"]) == 1


async def test_get_students_filter_decisions_multiple(database_with_data: AsyncSession, auth_client: AuthClient):
    """tests get students based on multiple decisions"""
    edition: Edition = (await database_with_data.execute(select(Edition))).scalars().all()[0]
    await auth_client.coach(edition)
    async with auth_client:
        response = await auth_client.get(
            "/editions/ed2022/students?decisions=0&decisions=1", follow_redirects=True)
        print(response.content)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["students"]) == 2


async def test_get_students_own_suggestion(database_with_data: AsyncSession, auth_client: AuthClient):
    """test get student based on query paramter for getting the students you wrote a suggestion for"""
    edition: Edition = (await database_with_data.execute(select(Edition))).scalars().all()[0]
    await auth_client.coach(edition)
    async with auth_client:
        await auth_client.post("/editions/ed2022/students/2/suggestions",
                               json={"suggestion": 1, "argumentation": "test"})
        response = await auth_client.get(
            "/editions/ed2022/students?own_suggestions=true", follow_redirects=True)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()["students"]) == 1
        assert response.json()["students"][0]["studentId"] == 2


async def test_get_emails_student_no_authorization(database_with_data: AsyncSession, auth_client: AuthClient):
    """tests that you can't get the mails of a student when you aren't logged in"""
    async with auth_client:
        response = await auth_client.get("/editions/ed2022/students/1/emails")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_get_emails_student_coach(database_with_data: AsyncSession, auth_client: AuthClient):
    """tests that a coach can't get the mails of a student"""
    edition: Edition = (await database_with_data.execute(select(Edition))).scalars().all()[0]
    await auth_client.coach(edition)
    async with auth_client:
        response = await auth_client.get("/editions/ed2022/students/1/emails")
    assert response.status_code == status.HTTP_403_FORBIDDEN


async def test_get_emails_student_admin(database_with_data: AsyncSession, auth_client: AuthClient):
    """tests that an admin can get the mails of a student"""
    await auth_client.admin()
    async with auth_client:
        await auth_client.post("/editions/ed2022/students/emails",
                               json={"students_id": [1], "email_status": 1})
        response = await auth_client.get("/editions/ed2022/students/1/emails")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()["emails"]) == 1
        assert response.json()["student"]["studentId"] == 1
        response = await auth_client.get("/editions/ed2022/students/2/emails")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()["emails"]) == 0
        assert response.json()["student"]["studentId"] == 2


async def test_post_email_no_authorization(database_with_data: AsyncSession, auth_client: AuthClient):
    """tests user need to be loged in"""
    async with auth_client:
        response = await auth_client.post("/editions/ed2022/students/emails")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_post_email_coach(database_with_data: AsyncSession, auth_client: AuthClient):
    """tests user can't be a coach"""
    edition: Edition = (await database_with_data.execute(select(Edition))).scalars().all()[0]
    await auth_client.coach(edition)
    async with auth_client:
        response = await auth_client.post("/editions/ed2022/students/emails")
    assert response.status_code == status.HTTP_403_FORBIDDEN


async def test_post_email_applied(database_with_data: AsyncSession, auth_client: AuthClient):
    """test create email applied"""
    await auth_client.admin()
    async with auth_client:
        response = await auth_client.post("/editions/ed2022/students/emails",
                                          json={"students_id": [2], "email_status": 0})
    assert response.status_code == status.HTTP_201_CREATED
    assert EmailStatusEnum(
        response.json()["studentEmails"][0]["emails"][0]["decision"]) == EmailStatusEnum.APPLIED


async def test_post_email_awaiting_project(database_with_data: AsyncSession, auth_client: AuthClient):
    """test create email awaiting project"""
    await auth_client.admin()
    async with auth_client:
        response = await auth_client.post("/editions/ed2022/students/emails",
                                          json={"students_id": [2], "email_status": 1})
    assert response.status_code == status.HTTP_201_CREATED
    assert EmailStatusEnum(
        response.json()["studentEmails"][0]["emails"][0]["decision"]) == EmailStatusEnum.AWAITING_PROJECT


async def test_post_email_approved(database_with_data: AsyncSession, auth_client: AuthClient):
    """test create email applied"""
    await auth_client.admin()
    async with auth_client:
        response = await auth_client.post("/editions/ed2022/students/emails",
                                          json={"students_id": [2], "email_status": 2})
    assert response.status_code == status.HTTP_201_CREATED
    assert EmailStatusEnum(
        response.json()["studentEmails"][0]["emails"][0]["decision"]) == EmailStatusEnum.APPROVED


async def test_post_email_contract_confirmed(database_with_data: AsyncSession, auth_client: AuthClient):
    """test create email contract confirmed"""
    await auth_client.admin()
    async with auth_client:
        response = await auth_client.post("/editions/ed2022/students/emails",
                                          json={"students_id": [2], "email_status": 3})
    assert response.status_code == status.HTTP_201_CREATED
    assert EmailStatusEnum(
        response.json()["studentEmails"][0]["emails"][0]["decision"]) == EmailStatusEnum.CONTRACT_CONFIRMED


async def test_post_email_contract_declined(database_with_data: AsyncSession, auth_client: AuthClient):
    """test create email contract declined"""
    await auth_client.admin()
    async with auth_client:
        response = await auth_client.post("/editions/ed2022/students/emails",
                                          json={"students_id": [2], "email_status": 4})
    assert response.status_code == status.HTTP_201_CREATED
    assert EmailStatusEnum(
        response.json()["studentEmails"][0]["emails"][0]["decision"]) == EmailStatusEnum.CONTRACT_DECLINED


async def test_post_email_rejected(database_with_data: AsyncSession, auth_client: AuthClient):
    """test create email rejected"""
    await auth_client.admin()
    async with auth_client:
        response = await auth_client.post("/editions/ed2022/students/emails",
                                          json={"students_id": [2], "email_status": 5})
    assert response.status_code == status.HTTP_201_CREATED
    assert EmailStatusEnum(
        response.json()["studentEmails"][0]["emails"][0]["decision"]) == EmailStatusEnum.REJECTED


async def test_creat_email_for_ghost(database_with_data: AsyncSession, auth_client: AuthClient):
    """test create email for student that don't exist"""
    await auth_client.admin()
    async with auth_client:
        response = await auth_client.post("/editions/ed2022/students/emails",
                                          json={"students_id": [100], "email_status": 5})
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_create_email_student_in_other_edition_bulk(database_with_data: AsyncSession, auth_client: AuthClient):
    """test creating an email for a student not in this edition when sending them in bulk
    The expected result is that only the mails to students in that edition are sent, and the
    others are ignored
    """
    edition: Edition = Edition(year=2023, name="ed2023")
    database_with_data.add(edition)
    student: Student = Student(first_name="Mehmet", last_name="Dizdar", preferred_name="Mehmet",
                               email_address="mehmet.dizdar@example.com", phone_number="(787)-938-6216", alumni=True,
                               wants_to_be_student_coach=False, edition=edition, skills=[])
    database_with_data.add(student)
    await database_with_data.commit()
    await auth_client.admin()
    async with auth_client:
        response = await auth_client.post("/editions/ed2022/students/emails",
                                          json={"students_id": [1, student.student_id], "email_status": 5})

        # When sending a request for students that aren't in this edition,
        # it ignores them & creates emails for the rest instead
        assert response.status_code == status.HTTP_201_CREATED
        assert len(response.json()["studentEmails"]) == 1
        assert response.json()["studentEmails"][0]["student"]["studentId"] == 1


async def test_create_emails_readonly_edition(database_session: AsyncSession, auth_client: AuthClient):
    """Test sending emails in a readonly edition"""
    edition: Edition = Edition(year=2023, name="ed2023", readonly=True)
    database_session.add(edition)
    student: Student = Student(first_name="Mehmet", last_name="Dizdar", preferred_name="Mehmet",
                               email_address="mehmet.dizdar@example.com", phone_number="(787)-938-6216", alumni=True,
                               wants_to_be_student_coach=False, edition=edition, skills=[])
    database_session.add(student)
    await database_session.commit()
    await auth_client.admin()

    async with auth_client:
        response = await auth_client.post(f"/editions/{edition.name}/students/emails",
                                          json={"students_id": [student.student_id], "email_status": 5})
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


async def test_get_emails_no_authorization(database_with_data: AsyncSession, auth_client: AuthClient):
    """test get emails not loged in"""
    async with auth_client:
        response = await auth_client.get("/editions/ed2022/students/emails")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_get_emails_coach(database_with_data: AsyncSession, auth_client: AuthClient):
    """test get emails logged in as coach"""
    edition: Edition = (await database_with_data.execute(select(Edition))).scalars().all()[0]
    await auth_client.coach(edition)
    async with auth_client:
        response = await auth_client.post("/editions/ed2022/students/emails")
    assert response.status_code == status.HTTP_403_FORBIDDEN


async def test_get_emails(database_with_data: AsyncSession, auth_client: AuthClient):
    """test get emails"""
    await auth_client.admin()
    async with auth_client:
        await auth_client.post("/editions/ed2022/students/emails",
                               json={"students_id": [1], "email_status": 3})
        await auth_client.post("/editions/ed2022/students/emails",
                               json={"students_id": [2], "email_status": 5})
        response = await auth_client.get("/editions/ed2022/students/emails")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["studentEmails"]) == 2
    assert response.json()["studentEmails"][0]["student"]["studentId"] == 1
    assert response.json()["studentEmails"][0]["emails"][0]["decision"] == 3
    assert response.json()["studentEmails"][1]["student"]["studentId"] == 2
    assert response.json()["studentEmails"][1]["emails"][0]["decision"] == 5


async def test_emails_filter_first_name(database_with_data: AsyncSession, auth_client: AuthClient):
    """test get emails with filter first name"""
    await auth_client.admin()
    async with auth_client:
        await auth_client.post("/editions/ed2022/students/emails",
                               json={"students_id": [1], "email_status": 1})
        await auth_client.post("/editions/ed2022/students/emails",
                               json={"students_id": [2], "email_status": 1})
        response = await auth_client.get(
            "/editions/ed2022/students/emails?name=Jos", follow_redirects=True)
    assert len(response.json()["studentEmails"]) == 1
    assert response.json()["studentEmails"][0]["student"]["firstName"] == "Jos"


async def test_emails_filter_last_name(database_with_data: AsyncSession, auth_client: AuthClient):
    """test get emails with filter last name"""
    await auth_client.admin()
    async with auth_client:
        await auth_client.post("/editions/ed2022/students/emails",
                               json={"students_id": [1], "email_status": 1})
        await auth_client.post("/editions/ed2022/students/emails",
                               json={"students_id": [2], "email_status": 1})
        response = await auth_client.get(
            "/editions/ed2022/students/emails?name=Vermeulen", follow_redirects=True)
    assert len(response.json()["studentEmails"]) == 1
    assert response.json()[
        "studentEmails"][0]["student"]["lastName"] == "Vermeulen"


async def test_emails_filter_between_first_and_last_name(database_with_data: AsyncSession, auth_client: AuthClient):
    """test get emails with filter last name"""
    await auth_client.admin()
    async with auth_client:
        await auth_client.post("/editions/ed2022/students/emails",
                               json={"students_id": [1], "email_status": 1})
        await auth_client.post("/editions/ed2022/students/emails",
                               json={"students_id": [2], "email_status": 1})
        response = await auth_client.get(
            "/editions/ed2022/students/emails?name=os V", follow_redirects=True)
    assert len(response.json()["studentEmails"]) == 1
    assert response.json()[
        "studentEmails"][0]["student"]["firstName"] == "Jos"
    assert response.json()[
        "studentEmails"][0]["student"]["lastName"] == "Vermeulen"


async def test_emails_filter_emailstatus(database_with_data: AsyncSession, auth_client: AuthClient):
    """test to get all email status, and you only filter on the email send"""
    await auth_client.admin()
    async with auth_client:
        for i in range(0, 6):
            await auth_client.post("/editions/ed2022/students/emails",
                                   json={"students_id": [2], "email_status": i})
            response = await auth_client.get(
                f"/editions/ed2022/students/emails?email_status={i}", follow_redirects=True)
            assert len(response.json()["studentEmails"]) == 1
            if i > 0:
                response = await auth_client.get(
                    f"/editions/ed2022/students/emails?email_status={i - 1}", follow_redirects=True)
                assert len(response.json()["studentEmails"]) == 0


async def test_emails_filter_emailstatus_multiple_status(database_with_data: AsyncSession, auth_client: AuthClient):
    """test to get all email status with multiple status"""
    await auth_client.admin()
    async with auth_client:
        await auth_client.post("/editions/ed2022/students/emails",
                               json={"students_id": [2], "email_status": 1})
        await auth_client.post("/editions/ed2022/students/emails",
                               json={"students_id": [1], "email_status": 3})
        response = await auth_client.get(
            "/editions/ed2022/students/emails?email_status=3&email_status=1", follow_redirects=True)
    assert len(response.json()["studentEmails"]) == 2
    assert response.json()["studentEmails"][0]["student"]["studentId"] == 1
    assert response.json()["studentEmails"][1]["student"]["studentId"] == 2
