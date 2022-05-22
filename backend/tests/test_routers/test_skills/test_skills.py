from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database.models import Skill
from tests.utils.authorization import AuthClient


async def test_get_skills(database_session: AsyncSession, auth_client: AuthClient):
    """Performs tests on getting skills

    Args:
        database_session (Session): a connection with the database
        auth_client (AuthClient): a client used to do rest calls
    """
    await auth_client.admin()
    skill = Skill(name="Backend")
    database_session.add(skill)
    await database_session.commit()

    # Make the get request
    async with auth_client:
        response = await auth_client.get("/skills/", follow_redirects=True)

        assert response.status_code == status.HTTP_200_OK
        response = response.json()
        assert response["skills"][0]["name"] == "Backend"


async def test_create_skill(database_session: AsyncSession, auth_client: AuthClient):
    """Perform tests on creating skills

    Args:
        database_session (Session): a connection with the database
        auth_client (AuthClient): a client used to do rest calls
    """
    await auth_client.admin()

    # Make the post request
    async with auth_client:
        response = await auth_client.post("/skills", json={"name": "Backend"})
        assert response.status_code == status.HTTP_201_CREATED
        assert (await auth_client.get("/skills/", follow_redirects=True)).json()["skills"][0]["name"] == "Backend"


async def test_delete_skill(database_session: AsyncSession, auth_client: AuthClient):
    """Perform tests on deleting skills

    Args:
        database_session (Session): a connection with the database
        auth_client (AuthClient): a client used to do rest calls
    """
    await auth_client.admin()

    skill = Skill(name="Backend")
    database_session.add(skill)
    await database_session.commit()
    await database_session.refresh(skill)

    async with auth_client:
        response = await auth_client.delete(f"/skills/{skill.skill_id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_delete_skill_non_existing(database_session: AsyncSession, auth_client: AuthClient):
    """Delete a skill that doesn't exist"""
    await auth_client.admin()

    async with auth_client:
        response = await auth_client.delete("/skills/1")
        assert response.status_code == status.HTTP_404_NOT_FOUND
