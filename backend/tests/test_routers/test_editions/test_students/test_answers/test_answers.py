import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
#from starlette import status

#from settings import DB_PAGE_SIZE
from src.database.models import Edition, Project, User, Skill, ProjectRole, Student
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
    database_session.add(student01)
    database_session.add(student02)
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


async def test_get_answers(database_with_data: AsyncSession, auth_client: AuthClient):
    """test get answers"""
    async with auth_client:
        response = await auth_client.get("/editions/ed2023/students/1/answers", follow_redirects=True)
        print(response)
    assert False

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
