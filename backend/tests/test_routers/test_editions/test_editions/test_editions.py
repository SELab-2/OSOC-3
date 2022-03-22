from sqlalchemy.orm import Session
from starlette import status

from src.database.models import Edition
from tests.utils.authorization import AuthClient


def test_get_editions(database_session: Session, auth_client: AuthClient):
    """Perform tests on getting editions

    Args:
        database_session (Session): a connection with the database
        auth_client (AuthClient): a client used to do rest calls 
    """
    edition = Edition(year=2022)
    database_session.add(edition)
    database_session.commit()

    auth_client.coach(edition)

    # Make the get request
    response = auth_client.get("/editions/")

    assert response.status_code == status.HTTP_200_OK
    response = response.json()
    assert response["editions"][0]["year"] == 2022
    assert response["editions"][0]["editionId"] == 1


def test_get_edition_by_id(database_session: Session, auth_client: AuthClient):
    """Perform tests on getting editions by ids

    Args:
        database_session (Session): a connection with the database
        auth_client (AuthClient): a client used to do rest calls 
    """
    edition = Edition(year=2022)
    database_session.add(edition)
    database_session.commit()
    database_session.refresh(edition)

    auth_client.coach(edition)

    # Make the get request
    response = auth_client.get(f"/editions/{edition.edition_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["year"] == 2022
    assert response.json()["editionId"] == edition.edition_id


def test_create_edition(database_session: Session, auth_client: AuthClient):
    """Perform tests on creating editions

    Args:
        database_session (Session): a connection with the database
        auth_client (AuthClient): a client used to do rest calls 
    """
    auth_client.admin()

    # Verify that editions doesn't exist yet
    assert auth_client.get("/editions/1/").status_code == status.HTTP_404_NOT_FOUND

    # Make the post request
    response = auth_client.post("/editions/", json={"year": 2022})
    assert response.status_code == status.HTTP_201_CREATED
    assert auth_client.get("/editions/").json()["editions"][0]["year"] == 2022
    assert auth_client.get("/editions/").json()["editions"][0]["editionId"] == 1
    assert auth_client.get("/editions/1/").status_code == status.HTTP_200_OK


def test_create_edition_existing_year(database_session: Session, auth_client: AuthClient):
    """Test that creating an edition for a year that already exists throws an error"""
    auth_client.admin()

    response = auth_client.post("/editions/", json={"year": 2022})
    assert response.status_code == status.HTTP_201_CREATED

    # Try to make an edition in the same year
    response = auth_client.post("/editions/", json={"year": 2022})
    assert response.status_code == status.HTTP_409_CONFLICT


def test_delete_edition(database_session: Session, auth_client: AuthClient):
    """Perform tests on deleting editions

    Args:
        database_session (Session): a connection with the database
        auth_client (AuthClient): a client used to do rest calls 
    """
    auth_client.admin()

    edition = Edition(year=2022)
    database_session.add(edition)
    database_session.commit()
    database_session.refresh(edition)

    # Make the delete request
    response = auth_client.delete(f"/editions/{edition.edition_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_edition_non_existing(database_session: Session, auth_client: AuthClient):
    """Delete an edition that doesn't exist"""
    auth_client.admin()

    response = auth_client.delete("/edition/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND
