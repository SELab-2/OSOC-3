import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from settings import DB_PAGE_SIZE
from src.database.models import Edition, Project, User, Skill, ProjectRole, Student, Partner
from tests.utils.authorization import AuthClient


@pytest.fixture
async def database_with_data(database_session: AsyncSession) -> AsyncSession:
    """fixture for adding data to the database"""
    edition: Edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    project1 = Project(name="project1", edition=edition, number_of_students=2)
    project2 = Project(name="project2", edition=edition, number_of_students=3)
    project3 = Project(name="super nice project", edition=edition, number_of_students=3)
    database_session.add(project1)
    database_session.add(project2)
    database_session.add(project3)
    user: User = User(name="coach1")
    database_session.add(user)
    skill1: Skill = Skill(name="skill1", description="something about skill1")
    skill2: Skill = Skill(name="skill2", description="something about skill2")
    skill3: Skill = Skill(name="skill3", description="something about skill3")
    database_session.add(skill1)
    database_session.add(skill2)
    database_session.add(skill3)
    student01: Student = Student(first_name="Jos", last_name="Vermeulen", preferred_name="Joske",
                                 email_address="josvermeulen@mail.com", phone_number="0487/86.24.45", alumni=True,
                                 wants_to_be_student_coach=True, edition=edition, skills=[skill1, skill3])
    student02: Student = Student(first_name="Isabella", last_name="Christensen", preferred_name="Isabella",
                                 email_address="isabella.christensen@example.com", phone_number="98389723", alumni=True,
                                 wants_to_be_student_coach=True, edition=edition, skills=[skill2])
    project_role1: ProjectRole = ProjectRole(
        student=student01, project=project1, skill=skill1, drafter=user, argumentation="argmunet")
    project_role2: ProjectRole = ProjectRole(
        student=student01, project=project2, skill=skill3, drafter=user, argumentation="argmunet")
    project_role3: ProjectRole = ProjectRole(
        student=student02, project=project1, skill=skill1, drafter=user, argumentation="argmunet")
    database_session.add(project_role1)
    database_session.add(project_role2)
    database_session.add(project_role3)
    await database_session.commit()

    return database_session


@pytest.fixture
async def current_edition(database_with_data: AsyncSession) -> Edition:
    """fixture to get the latest edition"""
    return (await database_with_data.execute(select(Edition))).scalars().all()[-1]


async def test_get_projects(database_with_data: AsyncSession, auth_client: AuthClient):
    """Tests get all projects"""
    await auth_client.admin()
    async with auth_client:
        response = await auth_client.get("/editions/ed2022/projects", follow_redirects=True)
        print(f"response: {response}")
        json = response.json()
        print(f"json: {json}")
        assert len(json['projects']) == 3
        assert json['projects'][0]['name'] == "project1"
        assert json['projects'][1]['name'] == "project2"
        assert json['projects'][2]['name'] == "super nice project"


async def test_get_projects_paginated(database_session: AsyncSession, auth_client: AuthClient):
    """test get all projects paginated"""
    edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)

    for i in range(round(DB_PAGE_SIZE * 1.5)):
        database_session.add(Project(name=f"Project {i}", edition=edition, number_of_students=5))
    await database_session.commit()

    await auth_client.admin()
    async with auth_client:
        response = await auth_client.get("/editions/ed2022/projects?page=0", follow_redirects=True)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()['projects']) == DB_PAGE_SIZE
        response = await auth_client.get("/editions/ed2022/projects?page=1", follow_redirects=True)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()['projects']) == round(DB_PAGE_SIZE * 1.5) - DB_PAGE_SIZE


async def test_get_project(database_with_data: AsyncSession, auth_client: AuthClient):
    """Tests get a specific project"""
    await auth_client.admin()
    async with auth_client:
        response = await auth_client.get("/editions/ed2022/projects/1")
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json['name'] == 'project1'


async def test_delete_project(database_with_data: AsyncSession, auth_client: AuthClient):
    """Tests delete a project"""
    await auth_client.admin()
    async with auth_client:
        response = await auth_client.get("/editions/ed2022/projects/1")
        assert response.status_code == status.HTTP_200_OK
        response = await auth_client.delete("/editions/ed2022/projects/1")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        response = await auth_client.get("/editions/ed2022/projects/1")
        assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_delete_ghost_project(database_with_data: AsyncSession, auth_client: AuthClient):
    """Tests delete a project that doesn't exist"""
    await auth_client.admin()
    async with auth_client:
        response = await auth_client.get("/editions/ed2022/projects/400")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        response = await auth_client.delete("/editions/ed2022/projects/400")
        assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_create_project(database_with_data: AsyncSession, auth_client: AuthClient):
    """Tests creating a project"""
    await auth_client.admin()
    async with auth_client:
        response = await auth_client.get('/editions/ed2022/projects', follow_redirects=True)
        json = response.json()
        assert len(json['projects']) == 3
        assert len((await database_with_data.execute(select(Partner))).scalars().all()) == 0

        response = \
            await auth_client.post("/editions/ed2022/projects/",
                                   json={"name": "test",
                                         "number_of_students": 5,
                                         "skills": [1, 1, 1, 1, 1], "partners": ["ugent"], "coaches": [1]})
        print(response.json())
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['name'] == 'test'
        assert response.json()["partners"][0]["name"] == "ugent"

        assert len(database_with_data.query(Partner).all()) == 1

        response = await auth_client.get('/editions/ed2022/projects')
        json = response.json()

        assert len(json['projects']) == 4
        assert json['projects'][3]['name'] == "test"


async def test_create_project_same_partner(database_with_data: AsyncSession, auth_client: AuthClient):
    """Tests that creating a project doesn't create a partner if the partner already exists"""
    await auth_client.admin()
    assert len((await database_with_data.execute(select(Partner))).scalars().all()) == 0

    async with auth_client:
        await auth_client.post("/editions/ed2022/projects/",
                               json={"name": "test1",
                                     "number_of_students": 2,
                                     "skills": [1, 2], "partners": ["ugent"], "coaches": [1]})
        await auth_client.post("/editions/ed2022/projects/",
                               json={"name": "test2",
                                     "number_of_students": 2,
                                     "skills": [1, 2], "partners": ["ugent"], "coaches": [1]})
        assert len((await database_with_data.execute(select(Partner))).scalars().all()) == 1


async def test_create_project_non_existing_skills(database_with_data: AsyncSession, auth_client: AuthClient):
    """Tests creating a project with non-existing skills"""
    await auth_client.admin()
    async with auth_client:
        response = await auth_client.get('/editions/ed2022/projects', follow_redirects=True)

        json = response.json()
        assert len(json['projects']) == 3

        assert len((await database_with_data.execute(select(Skill).where(
            Skill.skill_id == 100))).scalars().all()) == 0

        response = await auth_client.post("/editions/ed2022/projects/",
                                          json={"name": "test1",
                                                "number_of_students": 1,
                                                "skills": [100], "partners": ["ugent"], "coaches": [1]})
        assert response.status_code == status.HTTP_404_NOT_FOUND

        response = await auth_client.get('/editions/ed2022/projects', follow_redirects=True)
        json = response.json()
        assert len(json['projects']) == 3


async def test_create_project_non_existing_coach(database_with_data: AsyncSession, auth_client: AuthClient):
    """Tests creating a project with a coach that doesn't exist"""
    await auth_client.admin()
    async with auth_client:
        response = await auth_client.get('/editions/ed2022/projects', follow_redirects=True)

        json = response.json()
        assert len(json['projects']) == 3

        assert len((await database_with_data.execute(select(Student).where(
            Student.edition_id == 10))).scalars().all()) == 0

        response = await auth_client.post("/editions/ed2022/projects/",
                                          json={"name": "test2",
                                                "number_of_students": 1,
                                                "skills": [100], "partners": ["ugent"], "coaches": [10]})
        assert response.status_code == status.HTTP_404_NOT_FOUND

        response = await auth_client.get('/editions/ed2022/projects', follow_redirects=True)
        json = response.json()
        assert len(json['projects']) == 3


async def test_create_project_no_name(database_with_data: AsyncSession, auth_client: AuthClient):
    """Tests creating a project that has no name"""
    await auth_client.admin()
    async with auth_client:
        response = await auth_client.get('/editions/ed2022/projects', follow_redirects=True)
        json = response.json()
        assert len(json['projects']) == 3
        response = \
            await auth_client.post("/editions/ed2022/projects/",
                                   # project has no name
                                   json={
                                       "number_of_students": 5,
                                       "skills": [], "partners": [], "coaches": []})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        response = await auth_client.get('/editions/ed2022/projects', follow_redirects=True)
        json = response.json()
        assert len(json['projects']) == 3


async def test_patch_project(database_with_data: AsyncSession, auth_client: AuthClient):
    """Tests patching a project"""
    await auth_client.admin()
    async with auth_client:
        response = await auth_client.get('/editions/ed2022/projects', follow_redirects=True)
        json = response.json()

        assert len(json['projects']) == 3

        response = await auth_client.patch("/editions/ed2022/projects/1",
                                           json={"name": "patched",
                                                 "number_of_students": 5,
                                                 "skills": [1, 1, 1, 1, 1], "partners": ["ugent"], "coaches": [1]})
        assert response.status_code == status.HTTP_204_NO_CONTENT

        response = await auth_client.get('/editions/ed2022/projects', follow_redirects=True)
        json = response.json()

        assert len(json['projects']) == 3
        assert json['projects'][0]['name'] == 'patched'


async def test_patch_project_non_existing_skills(database_with_data: AsyncSession, auth_client: AuthClient):
    """Tests patching a project with non-existing skills"""
    await auth_client.admin()
    assert len((await database_with_data.execute(select(Skill).where(
        Skill.skill_id == 100))).scalars().all()) == 0
    async with auth_client:
        response = await auth_client.patch("/editions/ed2022/projects/1",
                                           json={"name": "test1",
                                                 "number_of_students": 1,
                                                 "skills": [100], "partners": ["ugent"], "coaches": [1]})
        assert response.status_code == status.HTTP_404_NOT_FOUND

        response = await auth_client.get("/editions/ed2022/projects/1")
        json = response.json()
        assert 100 not in json["skills"]


async def test_patch_project_non_existing_coach(database_with_data: AsyncSession, auth_client: AuthClient):
    """Tests patching a project with a coach that doesn't exist"""
    await auth_client.admin()
    assert len((await database_with_data.execute(select(Student).where(
        Student.edition_id == 10))).scalars().all()) == 0

    async with auth_client:
        response = await auth_client.patch("/editions/ed2022/projects/1",
                                           json={"name": "test2",
                                                 "number_of_students": 1,
                                                 "skills": [100], "partners": ["ugent"], "coaches": [10]})
        assert response.status_code == status.HTTP_404_NOT_FOUND
        response = await auth_client.get("/editions/ed2022/projects/1")
        json = response.json()
        assert 10 not in json["coaches"]


async def test_patch_wrong_project(database_session: AsyncSession, auth_client: AuthClient):
    """Tests patching with wrong project info"""
    await auth_client.admin()
    database_session.add(Edition(year=2022, name="ed2022"))
    project = Project(name="project", edition_id=1,
                      project_id=1, number_of_students=2)
    database_session.add(project)
    await database_session.commit()

    async with auth_client:
        response = \
            await auth_client.patch("/editions/ed2022/projects/1",
                                    json={"name": "patched",
                                          "skills": [], "partners": [], "coaches": []})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        response2 = await auth_client.get('/editions/ed2022/projects', follow_redirects=True)
        json = response2.json()

        assert len(json['projects']) == 1
        assert json['projects'][0]['name'] == 'project'


async def test_create_project_old_edition(database_with_data: AsyncSession, auth_client: AuthClient):
    """test create a project for a readonly edition"""
    await auth_client.admin()
    database_with_data.add(Edition(year=2023, name="ed2023"))
    await database_with_data.commit()
    async with auth_client:
        response = \
            await auth_client.post("/editions/ed2022/projects/",
                                   json={"name": "test",
                                         "number_of_students": 5,
                                         "skills": [1, 1, 1, 1, 1], "partners": ["ugent"], "coaches": [1]})

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


async def test_search_project_name(database_with_data: AsyncSession, auth_client: AuthClient):
    """test search project on name"""
    await auth_client.admin()
    async with auth_client:
        response = await auth_client.get("/editions/ed2022/projects/?name=super")
        assert len(response.json()["projects"]) == 1
        assert response.json()["projects"][0]["name"] == "super nice project"


async def test_search_project_coach(database_with_data: AsyncSession, auth_client: AuthClient):
    """test search project on coach"""
    await auth_client.admin()
    user: User = (await database_with_data.execute(select(User).where(User.name == "Pytest Admin"))).scalar_one()
    async with auth_client:
        await auth_client.post("/editions/ed2022/projects/",
                               json={"name": "test",
                                     "number_of_students": 2,
                                     "skills": [1, 1, 1, 1, 1], "partners": ["ugent"], "coaches": [user.user_id]})
        response = await auth_client.get("/editions/ed2022/projects/?coach=true")
        assert len(response.json()["projects"]) == 1
        assert response.json()["projects"][0]["name"] == "test"
        assert response.json()["projects"][0]["coaches"][0]["userId"] == user.user_id
