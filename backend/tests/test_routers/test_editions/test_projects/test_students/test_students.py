import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database.models import Edition, Project, User, Skill, ProjectRole, Student
from tests.utils.authorization import AuthClient


@pytest.fixture
async def database_with_data(database_session: AsyncSession) -> AsyncSession:
    """fixture for adding data to the database"""
    edition: Edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    skill1: Skill = Skill(name="skill1", description="something about skill1")
    skill2: Skill = Skill(name="skill2", description="something about skill2")
    skill3: Skill = Skill(name="skill3", description="something about skill3")
    skill4: Skill = Skill(name="skill4", description="something about skill4")
    skill5: Skill = Skill(name="skill5", description="something about skill5")
    database_session.add(skill1)
    database_session.add(skill2)
    database_session.add(skill3)
    database_session.add(skill4)
    database_session.add(skill5)
    project1 = Project(name="project1", edition=edition, number_of_students=4, skills=[skill1, skill2, skill3, skill4, skill5])
    project2 = Project(name="project2", edition=edition, number_of_students=3, skills=[skill1, skill2, skill3, skill4])
    project3 = Project(name="project3", edition=edition, number_of_students=3, skills=[skill1, skill2, skill3])
    database_session.add(project1)
    database_session.add(project2)
    database_session.add(project3)
    user: User = User(name="coach1")
    database_session.add(user)
    student01: Student = Student(first_name="Jos", last_name="Vermeulen", preferred_name="Joske",
                                 email_address="josvermeulen@mail.com", phone_number="0487/86.24.45", alumni=True,
                                 wants_to_be_student_coach=True, edition=edition, skills=[skill1, skill3, skill4])
    student02: Student = Student(first_name="Isabella", last_name="Christensen", preferred_name="Isabella",
                                 email_address="isabella.christensen@example.com", phone_number="98389723", alumni=True,
                                 wants_to_be_student_coach=True, edition=edition, skills=[skill2, skill4])
    student03: Student = Student(first_name="Lotte", last_name="Buss", preferred_name="Lotte",
                                 email_address="lotte.buss@example.com", phone_number="0284-0749932", alumni=False,
                                 wants_to_be_student_coach=False, edition=edition, skills=[skill2, skill3, skill4])
    student04: Student = Student(first_name="Max", last_name="Tester", preferred_name="Mxa",
                                 email_address="max.test@example.com", phone_number="0284-1356832", alumni=False,
                                 wants_to_be_student_coach=False, edition=edition, skills=[skill5])
    database_session.add(student01)
    database_session.add(student02)
    database_session.add(student03)
    database_session.add(student04)
    project_role1: ProjectRole = ProjectRole(
        student=student01, project=project1, skill=skill1, drafter=user, argumentation="argmunet")
    project_role2: ProjectRole = ProjectRole(
        student=student01, project=project2, skill=skill3, drafter=user, argumentation="argmunet")
    project_role3: ProjectRole = ProjectRole(
        student=student02, project=project1, skill=skill2, drafter=user, argumentation="argmunet")
    project_role4: ProjectRole = ProjectRole(
        student=student04, project=project1, skill=skill5, drafter=user, argumentation="argmunet", definitive=True)
    database_session.add(project_role1)
    database_session.add(project_role2)
    database_session.add(project_role3)
    database_session.add(project_role4)
    await database_session.commit()

    return database_session


@pytest.fixture
async def current_edition(database_with_data: AsyncSession) -> Edition:
    """fixture to get the latest edition"""
    return (await database_with_data.execute(select(Edition))).scalars().all()[-1]


async def test_add_student_project(database_with_data: AsyncSession, current_edition: Edition, auth_client: AuthClient):
    """tests add a student to a project"""
    await auth_client.coach(current_edition)

    async with auth_client:
        resp = await auth_client.post(
            "/editions/ed2022/projects/1/students/3", json={"skill_id": 3})

        assert resp.status_code == status.HTTP_201_CREATED

        response2 = await auth_client.get('/editions/ed2022/projects', follow_redirects=True)
        json = response2.json()
        assert len(json['projects'][0]['projectRoles']) == 4
        assert json['projects'][0]['projectRoles'][3]['skillId'] == 3


async def test_add_ghost_student_project(database_with_data: AsyncSession, current_edition: Edition, auth_client: AuthClient):
    """Tests adding a non-existing student to a project"""
    await auth_client.coach(current_edition)

    student10: list[Student] = (await database_with_data.execute(select(Student).where(Student.student_id == 10)))\
        .scalars().all()
    assert len(student10) == 0

    async with auth_client:
        response = await auth_client.get('/editions/ed2022/projects/1')
        json = response.json()
        assert len(json['projectRoles']) == 3

        resp = await auth_client.post(
            "/editions/ed2022/projects/1/students/10", json={"skill_id": 3})
        assert resp.status_code == status.HTTP_404_NOT_FOUND

        response = await auth_client.get('/editions/ed2022/projects/1')
        json = response.json()
        assert len(json['projectRoles']) == 3


async def test_add_student_project_non_existing_skill(database_with_data: AsyncSession, current_edition: Edition, auth_client: AuthClient):
    """Tests adding a non-existing student to a project"""
    await auth_client.coach(current_edition)

    skill10: list[Skill] = (await database_with_data.execute(select(
        Skill).where(Skill.skill_id == 10))).scalars().all()
    assert len(skill10) == 0
    async with auth_client:
        response = await auth_client.get('/editions/ed2022/projects/1')
        json = response.json()
        assert len(json['projectRoles']) == 3

        resp = await auth_client.post(
        "/editions/ed2022/projects/1/students/3", json={"skill_id": 10})
        assert resp.status_code == status.HTTP_404_NOT_FOUND

        response = await auth_client.get('/editions/ed2022/projects/1')
        json = response.json()
        assert len(json['projectRoles']) == 3


async def test_add_student_to_ghost_project(database_with_data: AsyncSession, current_edition: Edition, auth_client: AuthClient):
    """Tests adding a student to a project that doesn't exist"""
    await auth_client.coach(current_edition)
    project10: list[Project] = (await database_with_data.execute(select(
        Project).where(Project.project_id == 10))).scalars().all()
    assert len(project10) == 0

    async with auth_client:
        resp = await auth_client.post(
            "/editions/ed2022/projects/10/students/1", json={"skill_id": 1})
        assert resp.status_code == status.HTTP_404_NOT_FOUND


async def test_add_incomplete_data_student_project(database_session: AsyncSession, auth_client: AuthClient):
    """Tests adding a student with incomplete data"""

    edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    project = Project(name="project", edition_id=1,
                      project_id=1, number_of_students=2)
    database_session.add(project)
    await database_session.commit()

    await auth_client.coach(edition)
    async with auth_client:
        resp = await auth_client.post(
            "/editions/ed2022/projects/1/students/1", json={})

        assert resp.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        response2 = await auth_client.get('/editions/ed2022/projects', follow_redirects=True)
        json = response2.json()

        assert len(json['projects'][0]['projectRoles']) == 0


async def test_change_student_project(database_with_data: AsyncSession, current_edition: Edition, auth_client: AuthClient):
    """Tests changing a student's project"""
    await auth_client.coach(current_edition)

    async with auth_client:
        resp1 = await auth_client.patch(
            "/editions/ed2022/projects/1/students/1", json={"skill_id": 4})

        assert resp1.status_code == status.HTTP_204_NO_CONTENT

        response2 = await auth_client.get('/editions/ed2022/projects', follow_redirects=True)
        json = response2.json()

        assert len(json['projects'][0]['projectRoles']) == 3
        assert json['projects'][0]['projectRoles'][0]['skillId'] == 4


async def test_change_incomplete_data_student_project(database_with_data: AsyncSession, current_edition: Edition, auth_client: AuthClient):
    """Tests changing a student's project with incomplete data"""
    await auth_client.coach(current_edition)

    async with auth_client:
        resp1 = await auth_client.patch(
            "/editions/ed2022/projects/1/students/1", json={})

        assert resp1.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        response2 = await auth_client.get('/editions/ed2022/projects', follow_redirects=True)
        json = response2.json()

        assert len(json['projects'][0]['projectRoles']) == 3
        assert json['projects'][0]['projectRoles'][0]['skillId'] == 1


async def test_change_ghost_student_project(database_with_data: AsyncSession, current_edition: Edition, auth_client: AuthClient):
    """Tests changing a non-existing student of a project"""
    await auth_client.coach(current_edition)

    student10: list[Student] = (await database_with_data.execute(select(
        Student).where(Student.student_id == 10))).scalars().all()
    assert len(student10) == 0
    async with auth_client:
        response = await auth_client.get('/editions/ed2022/projects/1')
        json = response.json()
        assert len(json['projectRoles']) == 3

        resp = await auth_client.patch(
            "/editions/ed2022/projects/1/students/10", json={"skill_id": 4})
        assert resp.status_code == status.HTTP_404_NOT_FOUND

        response = await auth_client.get('/editions/ed2022/projects/1')
        json = response.json()
        assert len(json['projectRoles']) == 3


async def test_change_student_project_non_existing_skill(database_with_data: AsyncSession, current_edition: Edition, auth_client: AuthClient):
    """Tests deleting a student from a project that isn't assigned"""
    await auth_client.coach(current_edition)

    skill10: list[Skill] = (await database_with_data.execute(select(
        Skill).where(Skill.skill_id == 10))).scalars().all()
    assert len(skill10) == 0

    async with auth_client:
        response = await auth_client.get('/editions/ed2022/projects/1')
        json = response.json()
        assert len(json['projectRoles']) == 3

        resp = await auth_client.patch(
            "/editions/ed2022/projects/1/students/3", json={"skill_id": 10})
        assert resp.status_code == status.HTTP_404_NOT_FOUND

        response = await auth_client.get('/editions/ed2022/projects/1')
        json = response.json()
        assert len(json['projectRoles']) == 3


async def test_change_student_project_ghost_drafter(database_with_data: AsyncSession, current_edition: Edition, auth_client: AuthClient):
    """Tests changing a drafter of a ProjectRole to a non-existing one"""
    await auth_client.coach(current_edition)
    user10: list[User] = (await database_with_data.execute(select(
        User).where(User.user_id == 10))).scalars().all()
    assert len(user10) == 0

    async with auth_client:
        response = await auth_client.get('/editions/ed2022/projects/1')
        json = response.json()
        assert len(json['projectRoles']) == 3

        resp = await auth_client.patch(
            "/editions/ed2022/projects/1/students/3", json={"skill_id": 4})
        assert resp.status_code == status.HTTP_404_NOT_FOUND

        response = await auth_client.get('/editions/ed2022/projects/1')
        json = response.json()
        assert len(json['projectRoles']) == 3


async def test_change_student_to_ghost_project(database_with_data: AsyncSession, current_edition: Edition, auth_client: AuthClient):
    """Tests changing a student of a project that doesn't exist"""
    await auth_client.coach(current_edition)
    project10: list[Project] = (await database_with_data.execute(select(
        Project).where(Project.project_id == 10))).scalars().all()
    assert len(project10) == 0

    async with auth_client:
        resp = await auth_client.patch(
            "/editions/ed2022/projects/10/students/1", json={"skill_id": 1})
        assert resp.status_code == status.HTTP_404_NOT_FOUND


async def test_delete_student_project(database_with_data: AsyncSession, current_edition: Edition, auth_client: AuthClient):
    """Tests deleting a student from a project"""
    await auth_client.coach(current_edition)
    async with auth_client:
        resp = await auth_client.delete("/editions/ed2022/projects/1/students/1")

        assert resp.status_code == status.HTTP_204_NO_CONTENT

        response2 = await auth_client.get('/editions/ed2022/projects', follow_redirects=True)
        json = response2.json()

        assert len(json['projects'][0]['projectRoles']) == 2


async def test_delete_student_project_empty(database_session: AsyncSession, auth_client: AuthClient):
    """Tests deleting a student from a project that isn't assigned"""

    edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    project = Project(name="project", edition_id=1,
                      project_id=1, number_of_students=2)
    database_session.add(project)
    await database_session.commit()

    await auth_client.coach(edition)
    async with auth_client:
        resp = await auth_client.delete("/editions/ed2022/projects/1/students/1")

        assert resp.status_code == status.HTTP_404_NOT_FOUND


async def test_get_conflicts(database_with_data: AsyncSession, current_edition: Edition, auth_client: AuthClient):
    """Test getting the conflicts"""
    await auth_client.coach(current_edition)
    async with auth_client:
        response = await auth_client.get("/editions/ed2022/projects/conflicts")
        json = response.json()
    assert len(json['conflictStudents']) == 1
    assert json['conflictStudents'][0]['student']['studentId'] == 1
    assert len(json['conflictStudents'][0]['projects']) == 2


async def test_add_student_project_old_edition(database_with_data: AsyncSession, auth_client: AuthClient):
    """tests add a student to a project from an old edition"""
    await auth_client.admin()
    database_with_data.add(Edition(year=2023, name="ed2023"))
    await database_with_data.commit()

    async with auth_client:
        resp = await auth_client.post(
            "/editions/ed2022/projects/1/students/3", json={"skill_id": 1, "drafter_id": 1})

    assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


async def test_add_student_same_project_role(database_with_data: AsyncSession, current_edition: Edition, auth_client: AuthClient):
    """Two different students can't have the same project_role"""
    await auth_client.coach(current_edition)

    async with auth_client:
        resp = await auth_client.post(
            "/editions/ed2022/projects/1/students/3", json={"skill_id": 2})

    assert resp.status_code == status.HTTP_400_BAD_REQUEST


async def test_add_student_project_wrong_project_skill(database_with_data: AsyncSession, current_edition: Edition, auth_client: AuthClient):
    """A project_role can't be created if the project doesn't require the skill"""
    await auth_client.coach(current_edition)

    async with auth_client:
        resp = await auth_client.post(
            "/editions/ed2022/projects/3/students/3", json={"skill_id": 4})

    assert resp.status_code == status.HTTP_400_BAD_REQUEST


async def test_add_student_project_wrong_student_skill(database_with_data: AsyncSession, current_edition: Edition, auth_client: AuthClient):
    """A project_role can't be created if the student doesn't have the skill"""
    await auth_client.coach(current_edition)

    async with auth_client:
        resp = await auth_client.post(
            "/editions/ed2022/projects/1/students/2", json={"skill_id": 1})

    assert resp.status_code == status.HTTP_400_BAD_REQUEST


async def test_add_student_project_already_confirmed(database_with_data: AsyncSession, current_edition: Edition, auth_client: AuthClient):
    """A project_role can't be cre created if the student involved has already been confirmed elsewhere"""
    await auth_client.coach(current_edition)

    async with auth_client:
        resp = await auth_client.post("/editions/ed2022/projects/1/students/4", json={"skill_id": 3})

    assert resp.status_code == status.HTTP_400_BAD_REQUEST


async def test_confirm_project_role(database_with_data: AsyncSession, auth_client: AuthClient):
    """Confirm a project role for a student without conflicts"""
    await auth_client.admin()

    async with auth_client:
        resp = await auth_client.post(
            "/editions/ed2022/projects/1/students/3", json={"skill_id": 3})

        assert resp.status_code == status.HTTP_201_CREATED

        response2 = await auth_client.post(
            "/editions/ed2022/projects/1/students/3/confirm")

        assert response2.status_code == status.HTTP_204_NO_CONTENT
    pr = (await database_with_data.execute(select(ProjectRole).where(ProjectRole.student_id == 3)
                                           .where(ProjectRole.project_id == 1))).scalar_one()
    assert pr.definitive is True


async def test_confirm_project_role_conflict(database_with_data: AsyncSession, auth_client: AuthClient):
    """A student who is part of a conflict can't have their project_role confirmed"""
    await auth_client.admin()
    async with auth_client:
        response2 = await auth_client.post(
            "/editions/ed2022/projects/1/students/1/confirm")

    assert response2.status_code == status.HTTP_409_CONFLICT
