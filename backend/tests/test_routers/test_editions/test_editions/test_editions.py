from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from settings import DB_PAGE_SIZE
from src.database.models import Edition
from tests.utils.authorization import AuthClient


async def test_get_editions(database_session: AsyncSession, auth_client: AuthClient):
    """Perform tests on getting editions

    Args:
        database_session (Session): a connection with the database
        auth_client (AuthClient): a client used to do rest calls
    """
    edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    await database_session.commit()

    await auth_client.coach(edition)

    # Make the get request
    async with auth_client:
        response = await auth_client.get("/editions/")


    assert response.status_code == status.HTTP_200_OK
    response = response.json()
    assert response["editions"][0]["year"] == 2022
    assert response["editions"][0]["editionId"] == 1
    assert response["editions"][0]["name"] == "ed2022"


async def test_get_editions_paginated(database_session: AsyncSession, auth_client: AuthClient):
    """Perform tests on getting paginated editions"""
    for i in range(round(DB_PAGE_SIZE * 1.5)):
        database_session.add(Edition(name=f"Project {i}", year=i))
    await database_session.commit()

    await auth_client.admin()

    async with auth_client:
        response = await auth_client.get("/editions?page=0", follow_redirects=True)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()['editions']) == DB_PAGE_SIZE
        response = await auth_client.get("/editions?page=1", follow_redirects=True)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()['editions']) == round(DB_PAGE_SIZE * 1.5) - DB_PAGE_SIZE


async def test_get_edition_by_name_admin(database_session: AsyncSession, auth_client: AuthClient):
    """Test getting an edition as an admin"""
    await auth_client.admin()

    edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    await database_session.commit()

    async with auth_client:
        response = await auth_client.get(f"/editions/{edition.name}")
    assert response.status_code == status.HTTP_200_OK


async def test_get_edition_by_name_coach(database_session: AsyncSession, auth_client: AuthClient):
    """Perform tests on getting editions by ids

    Args:
        database_session (Session): a connection with the database
        auth_client (AuthClient): a client used to do rest calls
    """
    edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    await database_session.commit()

    await auth_client.coach(edition)

    # Make the get request
    async with auth_client:
        response = await auth_client.get(f"/editions/{edition.name}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["year"] == 2022
        assert response.json()["editionId"] == edition.edition_id
        assert response.json()["name"] == edition.name


async def test_get_edition_by_name_unauthorized(database_session: AsyncSession, auth_client: AuthClient):
    """Test getting an edition without access token"""
    edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    await database_session.commit()

    async with auth_client:
        response = await auth_client.get("/editions/ed2022")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_get_edition_by_name_not_coach(database_session: AsyncSession, auth_client: AuthClient):
    """Test getting an edition without being a coach in it"""
    edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)

    coach_edition = Edition(year=2021, name="ed2021")
    database_session.add(coach_edition)

    await database_session.commit()

    # Sign in as a coach in a different edition
    await auth_client.coach(coach_edition)

    async with auth_client:
        response = await auth_client.get(f"/editions/{edition.name}")
    assert response.status_code == status.HTTP_403_FORBIDDEN


async def test_create_edition_admin(database_session: AsyncSession, auth_client: AuthClient):
    """Test creating an edition as an admin"""
    await auth_client.admin()

    async with auth_client:
        # Verify that editions doesn't exist yet
        response = await auth_client.get("/editions/ed2022")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        # Make the post request
        response = await auth_client.post("/editions/", json={"year": 2022, "name": "ed2022"})
        assert response.status_code == status.HTTP_201_CREATED
        response = await auth_client.get("/editions/")
        assert response.json()["editions"][0]["year"] == 2022
        assert response.json()["editions"][0]["editionId"] == 1
        assert response.json()["editions"][0]["name"] == "ed2022"
        response = await auth_client.get("/editions/ed2022")
        assert response.status_code == status.HTTP_200_OK


async def test_create_edition_unauthorized(database_session: AsyncSession, auth_client: AuthClient):
    """Test creating an edition without any credentials"""
    async with auth_client:
        response = await auth_client.post("/editions/", json={"year": 2022, "name": "ed2022"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_create_edition_coach(database_session: AsyncSession, auth_client: AuthClient):
    """Test creating an edition as a coach"""
    edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    await database_session.commit()

    await auth_client.coach(edition)
    async with auth_client:
        response = await auth_client.post("/editions/", json={"year": 2022, "name": "ed2022"})
    assert response.status_code == status.HTTP_403_FORBIDDEN


async def test_create_edition_existing_year(database_session: AsyncSession, auth_client: AuthClient):
    """Test that creating an edition for a year that already exists throws an error"""
    await auth_client.admin()

    async with auth_client:
        response = await auth_client.post("/editions/", json={"year": 2022, "name": "ed2022"})
        assert response.status_code == status.HTTP_201_CREATED
        # Try to make an edition in the same year
        response = await auth_client.post("/editions/", json={"year": 2022, "name": "ed2022"})
        assert response.status_code == status.HTTP_409_CONFLICT


async def test_create_edition_malformed(database_session: AsyncSession, auth_client: AuthClient):
    await auth_client.admin()

    async with auth_client:
        response = await auth_client.post("/editions/", json={"year": 2023, "name": "Life is fun"})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_delete_edition_admin(database_session: AsyncSession, auth_client: AuthClient):
    """Perform tests on deleting editions

    Args:
        database_session (Session): a connection with the database
        auth_client (AuthClient): a client used to do rest calls
    """
    await auth_client.admin()

    edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    await database_session.commit()

    async with auth_client:
        # Make the delete request
        response = await auth_client.delete(f"/editions/{edition.name}")
        assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_delete_edition_unauthorized(database_session: AsyncSession, auth_client: AuthClient):
    """Test deleting an edition without any credentials"""
    edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    await database_session.commit()

    async with auth_client:
        # Make the delete request
        assert (await auth_client.delete(f"/editions/{edition.name}")).status_code == status.HTTP_401_UNAUTHORIZED


async def test_delete_edition_coach(database_session: AsyncSession, auth_client: AuthClient):
    """Test deleting an edition as a coach"""
    edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    await database_session.commit()

    await auth_client.coach(edition)

    async with auth_client:
        # Make the delete request
        assert (await auth_client.delete(f"/editions/{edition.name}")).status_code == status.HTTP_403_FORBIDDEN


async def test_delete_edition_non_existing(database_session: AsyncSession, auth_client: AuthClient):
    """Delete an edition that doesn't exist"""
    await auth_client.admin()

    async with auth_client:
        response = await auth_client.delete("/edition/doesnotexist")
        assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_get_editions_limited_permission(database_session: AsyncSession, auth_client: AuthClient):
    """A coach should only see the editions they are drafted for"""
    edition = Edition(year=2022, name="ed2022")
    edition2 = Edition(year=2023, name="ed2023")
    database_session.add(edition)
    database_session.add(edition2)
    await database_session.commit()

    await auth_client.coach(edition)

    async with auth_client:
        # Make the get request
        response = await auth_client.get("/editions/")

    assert response.status_code == status.HTTP_200_OK
    response = response.json()
    assert response["editions"][0]["year"] == 2022
    assert response["editions"][0]["editionId"] == 1
    assert response["editions"][0]["name"] == "ed2022"
    assert len(response["editions"]) == 1


async def test_get_edition_by_name_coach_not_assigned(database_session: AsyncSession, auth_client: AuthClient):
    """A coach not assigned to the edition should not be able to see it"""
    edition = Edition(year=2022, name="ed2022")
    edition2 = Edition(year=2023, name="ed2023")
    database_session.add(edition)
    database_session.add(edition2)
    await database_session.commit()

    await auth_client.coach(edition)

    async with auth_client:
        # Make the get request
        response = await auth_client.get(f"/editions/{edition2.name}")
    assert response.status_code == status.HTTP_403_FORBIDDEN
