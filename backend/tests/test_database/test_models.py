from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import models


async def test_user_coach_request(database_session: AsyncSession):
    """Test sending a coach request"""
    edition = models.Edition(year=2022, name="ed2022")
    database_session.add(edition)
    await database_session.commit()

    # Passing as user_id
    user = models.User(name="name")
    database_session.add(user)
    await database_session.commit()

    req = models.CoachRequest(user_id=user.user_id, edition=edition)
    database_session.add(req)
    await database_session.commit()

    assert req.user == user

    # Check if passing as user instead of user_id works
    user = models.User(name="name")
    database_session.add(user)
    await database_session.commit()

    req = models.CoachRequest(user=user, edition=edition)
    database_session.add(req)
    await database_session.commit()

    assert req.user_id == user.user_id


async def test_project_partners(database_session: AsyncSession):
    """Test adding a partner to a project"""
    project = models.Project(name="project")
    database_session.add(project)
    await database_session.commit()

    partner = models.Partner(name="partner")
    database_session.add(partner)
    await database_session.commit()

    # query the partner and the project to create the association tables
    (await database_session.execute(select(models.Partner).where(models.Partner.partner_id == partner.partner_id))).unique().scalars().one()
    (await database_session.execute(
        select(models.Project).where(models.Project.project_id == project.project_id))).unique().scalars().one()

    assert len(partner.projects) == 0
    assert len(project.partners) == 0

    partner.projects.append(project)
    await database_session.commit()

    # Verify that appending to the list updates the association table
    # in both directions
    assert len(partner.projects) == 1
    assert partner.projects[0] == project

    assert len(project.partners) == 1
    assert project.partners[0] == partner
