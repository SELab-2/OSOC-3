import pytest
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from settings import DB_PAGE_SIZE
from src.app.schemas.projects import InputProject, QueryParamsProjects
import src.database.crud.projects as crud
from src.database.models import Edition, Partner, Project, User, Skill, ProjectRole, Student, ProjectRoleSuggestion


@pytest.fixture
async def database_with_data(database_session: AsyncSession) -> AsyncSession:
    """fixture for adding data to the database"""
    edition: Edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    user: User = User(name="coach1")
    database_session.add(user)
    project1 = Project(name="project1", edition=edition)
    project2 = Project(name="project2", edition=edition)
    project3 = Project(name="super nice project", edition=edition, coaches=[user])
    database_session.add(project1)
    database_session.add(project2)
    database_session.add(project3)
    skill1: Skill = Skill(name="skill1")
    skill2: Skill = Skill(name="skill2")
    skill3: Skill = Skill(name="skill3")
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


async def test_get_all_projects_empty(database_session: AsyncSession):
    """test get all projects but there are none"""
    edition: Edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    await database_session.commit()
    projects: list[Project] = await crud.get_projects_for_edition(
        database_session, edition)
    assert len(projects) == 0


async def test_get_all_projects(database_session: AsyncSession):
    """test get all projects"""
    edition: Edition = Edition(year=2022, name="ed2022")
    for i in range(DB_PAGE_SIZE - 1):
        database_session.add(Project(name=f"Project {i}", edition=edition))
    await database_session.commit()

    projects: list[Project] = await crud.get_projects_for_edition(database_session, edition)
    assert len(projects) == DB_PAGE_SIZE - 1


async def test_get_all_projects_pagination(database_session: AsyncSession):
    """test get all projects paginated"""
    edition = Edition(year=2022, name="ed2022")
    user: User = User(name="coach")
    database_session.add(user)

    for i in range(round(DB_PAGE_SIZE * 1.5)):
        database_session.add(Project(name=f"Project {i}", edition=edition))
    await database_session.commit()

    assert len(
        await crud.get_projects_for_edition_page(database_session, edition, QueryParamsProjects(page=0), user=user)
    ) == DB_PAGE_SIZE
    assert len(
        await crud.get_projects_for_edition_page(database_session, edition, QueryParamsProjects(page=1), user=user)
    ) == round(DB_PAGE_SIZE * 1.5) - DB_PAGE_SIZE


async def test_get_project_search_name(database_session: AsyncSession):
    """test get project with a specific name"""
    edition: Edition = Edition(year=2022, name="ed2022")
    user: User = User(name="coach")
    database_session.add(user)

    for i in range(DB_PAGE_SIZE - 2):
        database_session.add(Project(name=f"Project {i}", edition=edition))
    database_session.add(Project(name=f"nice project", edition=edition))
    await database_session.commit()

    projects: list[Project] = await crud.get_projects_for_edition_page(
        database_session, edition, QueryParamsProjects(name="nice"), user=user
    )
    assert len(projects) == 1
    assert projects[0].name == "nice project"


async def test_get_project_search_coach(database_session: AsyncSession):
    """test get projects that you are a coach"""
    edition: Edition = Edition(year=2022, name="ed2022")
    user: User = User(name="coach")
    database_session.add(user)

    for i in range(DB_PAGE_SIZE - 2):
        database_session.add(Project(name=f"Project {i}", edition=edition))
    database_session.add(Project(name=f"nice project", edition=edition, coaches=[user]))
    await database_session.commit()

    projects: list[Project] = await crud.get_projects_for_edition_page(
        database_session, edition, QueryParamsProjects(coach=True), user=user
    )
    assert len(projects) == 1


async def test_add_project(database_session: AsyncSession):
    """tests add a project when the project don't exist yet"""
    edition: Edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    await database_session.commit()

    partners: list[Partner] = [Partner(name="partner1"), Partner(name="partner2")]

    input_project: InputProject = InputProject(
        name="project 1",
        partners=["partner1", "partner2"],
        coaches=[]
    )

    project: Project = await crud.create_project(database_session, edition, input_project, partners=partners)

    assert len((await database_session.execute(select(Project))).unique().scalars().all()) == 1
    assert project.name == input_project.name
    assert len(project.partners) == len(partners)
    assert project.edition == edition


async def test_get_project_not_found(database_session: AsyncSession):
    """test project that don't exist"""
    with pytest.raises(NoResultFound):
        await crud.get_project(database_session, 500)


async def test_get_project(database_session: AsyncSession):
    """test get project"""
    edition: Edition = Edition(year=2022, name="ed2022")
    project: Project = Project(name="project 1", edition=edition)
    database_session.add(project)
    await database_session.commit()

    assert project == await crud.get_project(database_session, project.project_id)


async def test_delete_project_no_project_roles(database_session: AsyncSession):
    """test delete a project that don't have project roles"""
    edition: Edition = Edition(year=2022, name="ed2022")
    project: Project = Project(name="project 1", edition=edition)
    database_session.add(project)
    await database_session.commit()

    assert len((await database_session.execute(select(Project))).unique().scalars().all()) == 1
    await crud.delete_project(database_session, project)
    assert len((await database_session.execute(select(Project))).unique().scalars().all()) == 0


async def test_delete_project_with_project_roles(database_session: AsyncSession):
    """test delete a project that has project roles"""
    edition: Edition = Edition(year=2022, name="ed2022")
    project: Project = Project(
        name="project 1",
        edition=edition,
        project_roles=[ProjectRole(slots=1, skill=Skill(name="skill"))]
    )
    database_session.add(project)
    await database_session.commit()

    assert len((await database_session.execute(select(Project))).unique().scalars().all()) == 1
    assert len((await database_session.execute(select(ProjectRole))).unique().scalars().all()) == 1
    await crud.delete_project(database_session, project)
    assert len((await database_session.execute(select(Project))).unique().scalars().all()) == 0
    assert len((await database_session.execute(select(ProjectRole))).unique().scalars().all()) == 0


async def test_delete_project_role(database_session: AsyncSession):
    """test delete a project role"""
    edition: Edition = Edition(year=2022, name="ed2022")
    project: Project = Project(
        name="project 1",
        edition=edition,
        project_roles=[ProjectRole(slots=1, skill=Skill(name="skill"))]
    )
    database_session.add(project)
    await database_session.commit()
    assert len((await database_session.execute(select(ProjectRole))).unique().scalars().all()) == 1
    await crud.delete_project_role(database_session, 1)
    assert len((await database_session.execute(select(ProjectRole))).unique().scalars().all()) == 0


async def test_patch_project(database_session: AsyncSession):
    """tests patch a project"""
    edition: Edition = Edition(year=2022, name="ed2022")
    project: Project = Project(
        name="project 1",
        edition=edition,
        coaches=[User(name="coach 1")],
        partners=[Partner(name="partner 1")]
    )
    database_session.add(project)
    await database_session.commit()

    new_user = User(name="coach 2")
    new_partner = Partner(name="partner 2")
    database_session.add(new_user)
    database_session.add(new_partner)
    await database_session.commit()

    patch: InputProject = InputProject(
        name="project 1 - PATCHED",
        partners=[new_partner.name],
        coaches=[new_user.user_id]
    )

    await crud.patch_project(database_session, project, patch, [new_partner])
    assert project.name == "project 1 - PATCHED"
    assert len(project.partners) == 1
    assert len(project.coaches) == 1
    assert project.partners[0].name == new_partner.name
    assert project.coaches[0].user_id == new_user.user_id


async def test_get_conflict_students(database_session: AsyncSession):
    """test if the right ConflictStudent is given"""
    edition: Edition = Edition(year=2022, name="ed2022")
    skill: Skill = Skill(name="skill 1")
    student: Student = Student(
        first_name="Jos",
        last_name="Vermeulen",
        preferred_name="Joske",
        email_address="josvermeulen@mail.com",
        phone_number="0487/86.24.45",
        alumni=True,
        wants_to_be_student_coach=True,
        edition=edition
    )

    database_session.add(Student(
        first_name="Jos2",
        last_name="Vermeulen",
        preferred_name="Joske",
        email_address="josvermeulen@gmail.com",
        phone_number="0487/86.24.46",
        alumni=True,
        wants_to_be_student_coach=True,
        edition=edition
    ))

    database_session.add(ProjectRoleSuggestion(
        student=student,
        project_role=ProjectRole(
            skill=skill,
            slots=1,
            project=Project(
                name="project 1",
                edition=edition
            )
        )
    ))

    database_session.add(ProjectRoleSuggestion(
        student=student,
        project_role=ProjectRole(
            skill=skill,
            slots=1,
            project=Project(
                name="project 2",
                edition=edition
            )
        )
    ))
    await database_session.commit()

    conflicts: list[Student] = await crud.get_conflict_students(database_session, edition)
    assert len(conflicts) == 1
    assert conflicts[0].student_id == student.student_id
    assert len(conflicts[0].pr_suggestions) == 2
