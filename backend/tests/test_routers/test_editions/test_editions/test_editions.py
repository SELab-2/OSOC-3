from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
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
    response = auth_client.get("/editions/")

    assert response.status_code == status.HTTP_200_OK
    response = response.json()
    assert response["editions"][0]["year"] == 2022
    assert response["editions"][0]["editionId"] == 1
    assert response["editions"][0]["name"] == "ed2022"


def test_get_editions_paginated(database_session: Session, auth_client: AuthClient):
    """Perform tests on getting paginated editions"""
    for i in range(round(DB_PAGE_SIZE * 1.5)):
        database_session.add(Edition(name=f"Project {i}", year=i))
    database_session.commit()

    auth_client.admin()

    response = auth_client.get("/editions?page=0")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['editions']) == DB_PAGE_SIZE
    response = auth_client.get("/editions?page=1")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['editions']) == round(DB_PAGE_SIZE * 1.5) - DB_PAGE_SIZE


def test_get_edition_by_name_admin(database_session: Session, auth_client: AuthClient):
    """Test getting an edition as an admin"""
    auth_client.admin()

    edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    database_session.commit()

    response = auth_client.get(f"/editions/{edition.name}")
    assert response.status_code == status.HTTP_200_OK


def test_get_edition_by_name_coach(database_session: Session, auth_client: AuthClient):
    """Perform tests on getting editions by ids

    Args:
        database_session (Session): a connection with the database
        auth_client (AuthClient): a client used to do rest calls
    """
    edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    database_session.commit()

    auth_client.coach(edition)

    # Make the get request
    response = auth_client.get(f"/editions/{edition.name}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["year"] == 2022
    assert response.json()["editionId"] == edition.edition_id
    assert response.json()["name"] == edition.name


def test_get_edition_by_name_unauthorized(database_session: Session, auth_client: AuthClient):
    """Test getting an edition without access token"""
    edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    database_session.commit()

    assert auth_client.get("/editions/ed2022").status_code == status.HTTP_401_UNAUTHORIZED


def test_get_edition_by_name_not_coach(database_session: Session, auth_client: AuthClient):
    """Test getting an edition without being a coach in it"""
    edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)

    coach_edition = Edition(year=2021, name="ed2021")
    database_session.add(coach_edition)

    database_session.commit()

    # Sign in as a coach in a different edition
    auth_client.coach(coach_edition)

    assert auth_client.get(f"/editions/{edition.name}").status_code == status.HTTP_403_FORBIDDEN


def test_create_edition_admin(database_session: Session, auth_client: AuthClient):
    """Test creating an edition as an admin"""
    auth_client.admin()

    # Verify that editions doesn't exist yet
    assert auth_client.get("/editions/ed2022/").status_code == status.HTTP_404_NOT_FOUND

    # Make the post request
    response = auth_client.post("/editions/", json={"year": 2022, "name": "ed2022"})
    assert response.status_code == status.HTTP_201_CREATED
    assert auth_client.get("/editions/").json()["editions"][0]["year"] == 2022
    assert auth_client.get("/editions/").json()["editions"][0]["editionId"] == 1
    assert auth_client.get("/editions/").json()["editions"][0]["name"] == "ed2022"
    assert auth_client.get("/editions/ed2022/").status_code == status.HTTP_200_OK


def test_create_edition_unauthorized(database_session: Session, auth_client: AuthClient):
    """Test creating an edition without any credentials"""
    assert auth_client.post("/editions/", json={"year": 2022, "name": "ed2022"}).status_code == status.HTTP_401_UNAUTHORIZED


def test_create_edition_coach(database_session: Session, auth_client: AuthClient):
    """Test creating an edition as a coach"""
    edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    database_session.commit()

    auth_client.coach(edition)

    assert auth_client.post("/editions/", json={"year": 2022, "name": "ed2022"}).status_code == status.HTTP_403_FORBIDDEN


def test_create_edition_existing_year(database_session: Session, auth_client: AuthClient):
    """Test that creating an edition for a year that already exists throws an error"""
    auth_client.admin()

    response = auth_client.post("/editions/", json={"year": 2022, "name": "ed2022"})
    assert response.status_code == status.HTTP_201_CREATED

    # Try to make an edition in the same year
    response = auth_client.post("/editions/", json={"year": 2022, "name": "ed2022"})
    assert response.status_code == status.HTTP_409_CONFLICT


def test_create_edition_malformed(database_session: Session, auth_client: AuthClient):
    auth_client.admin()

    response = auth_client.post("/editions/", json={"year": 2023, "name": "Life is fun"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_edition_admin(database_session: Session, auth_client: AuthClient):
    """Perform tests on deleting editions

    Args:
        database_session (Session): a connection with the database
        auth_client (AuthClient): a client used to do rest calls
    """
    auth_client.admin()

    edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    database_session.commit()

    # Make the delete request
    response = auth_client.delete(f"/editions/{edition.name}")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_edition_unauthorized(database_session: Session, auth_client: AuthClient):
    """Test deleting an edition without any credentials"""
    edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    database_session.commit()

    # Make the delete request
    assert auth_client.delete(f"/editions/{edition.name}").status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_edition_coach(database_session: Session, auth_client: AuthClient):
    """Test deleting an edition as a coach"""
    edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    database_session.commit()

    auth_client.coach(edition)

    # Make the delete request
    assert auth_client.delete(f"/editions/{edition.name}").status_code == status.HTTP_403_FORBIDDEN


def test_delete_edition_non_existing(database_session: Session, auth_client: AuthClient):
    """Delete an edition that doesn't exist"""
    auth_client.admin()

    response = auth_client.delete("/edition/doesnotexist")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_editions_limited_permission(database_session: Session, auth_client: AuthClient):
    """A coach should only see the editions they are drafted for"""
    edition = Edition(year=2022, name="ed2022")
    edition2 = Edition(year=2023, name="ed2023")
    database_session.add(edition)
    database_session.add(edition2)
    database_session.commit()

    auth_client.coach(edition)

    # Make the get request
    response = auth_client.get("/editions/")

    assert response.status_code == status.HTTP_200_OK
    response = response.json()
    assert response["editions"][0]["year"] == 2022
    assert response["editions"][0]["editionId"] == 1
    assert response["editions"][0]["name"] == "ed2022"
    assert len(response["editions"]) == 1


def test_get_edition_by_name_coach_not_assigned(database_session: Session, auth_client: AuthClient):
    """A coach not assigned to the edition should not be able to see it"""
    edition = Edition(year=2022, name="ed2022")
    edition2 = Edition(year=2023, name="ed2023")
    database_session.add(edition)
    database_session.add(edition2)
    database_session.commit()

    auth_client.coach(edition)

    # Make the get request
    response = auth_client.get(f"/editions/{edition2.name}")
    assert response.status_code == status.HTTP_403_FORBIDDEN
