import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.exceptions.authentication import MissingPermissionsException
from src.app.exceptions.util import NotFound
from src.app.utils.dependencies import get_project_role, require_auth, require_coach_ws, get_project
from src.database.models import Edition, User, Project, ProjectRole, Skill


async def test_require_coach_ws(database_session: AsyncSession):
    """test require coach websockets"""
    edition: Edition = Edition(year=2022, name="ed22")
    database_session.add(edition)
    coach1: User = User(name="coach1", editions=[edition])
    coach2: User = User(name="coach2", editions=[])
    database_session.add(coach1)
    database_session.add(coach2)
    await database_session.commit()
    coach_ws: User = await require_coach_ws(edition=edition, user=coach1)
    assert coach_ws == coach1
    with pytest.raises(MissingPermissionsException):
        await require_auth(coach2)


async def test_project_wrong_edition(database_session: AsyncSession):
    """test project wrong edition"""
    edition1: Edition = Edition(year=2022, name="ed22")
    edition2: Edition = Edition(year=2023, name="ed23")
    database_session.add(edition1)
    database_session.add(edition2)
    project: Project = Project(name="Project", edition=edition1)
    database_session.add(project)
    await database_session.commit()
    with pytest.raises(NotFound):
        await get_project(1, database_session, edition2)


async def test_project_role_wrong_project(database_session: AsyncSession):
    """test project role wrong project"""
    edition1: Edition = Edition(year=2022, name="ed22")
    database_session.add(edition1)
    project1: Project = Project(name="Project1",
                                edition=edition1,
                                project_roles=[ProjectRole(slots=1, skill=Skill(name="skill"))])
    project2: Project = Project(name="Project2", edition=edition1)
    database_session.add(project1)
    database_session.add(project2)
    await database_session.commit()
    with pytest.raises(NotFound):
        await get_project_role(1, project2, database_session)
