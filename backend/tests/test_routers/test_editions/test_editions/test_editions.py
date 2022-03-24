from json import dumps
from sqlalchemy.orm import Session
from starlette import status
from starlette.testclient import TestClient

from src.database.models import Edition


def test_get_editions(database_session: Session, test_client: TestClient):
    """Performe tests on getting editions

    Args:
        database_session (Session): a connection with the database
        test_client (TestClient): a client used to do rest calls 
    """
    edition = Edition(year = 2022)
    database_session.add(edition)
    database_session.commit()

    # Make the get request
    response = test_client.get("/editions/")

    assert response.status_code == status.HTTP_200_OK
    response = response.json()
    assert response["editions"][0]["year"] == 2022
    assert response["editions"][0]["editionId"] == 1


def test_get_edition_by_id(database_session: Session, test_client: TestClient):
    """Performe tests on getting editions by ids

    Args:
        database_session (Session): a connection with the database
        test_client (TestClient): a client used to do rest calls 
    """
    edition = Edition(year = 2022)
    database_session.add(edition)
    database_session.commit()
    database_session.refresh(edition)

    # Make the get request
    response = test_client.get(f"/editions/{edition.edition_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["year"] == 2022
    assert response.json()["editionId"] == edition.edition_id


def test_create_edition(database_session: Session, test_client: TestClient):
    """Performe tests on creating editions

    Args:
        database_session (Session): a connection with the database
        test_client (TestClient): a client used to do rest calls 
    """
    # Verify that editions doesn't exist yet
    assert test_client.get("/editions/1/").status_code == status.HTTP_404_NOT_FOUND

    # Make the post request
    response = test_client.post("/editions/", json={"year": 2022})
    assert response.status_code == status.HTTP_201_CREATED
    assert test_client.get("/editions/").json()["editions"][0]["year"] == 2022
    assert test_client.get("/editions/").json()["editions"][0]["editionId"] == 1
    assert test_client.get("/editions/1/").status_code == status.HTTP_200_OK

    # Try to make an edition in the same year
    #response = test_client.post("/editions/", json={"year": 2022})
    #assert response.status_code == status.HTTP_409_CONFLICT


def test_delete_edition(database_session: Session, test_client: TestClient):
    """Performe tests on deleting editions

    Args:
        database_session (Session): a connection with the database
        test_client (TestClient): a client used to do rest calls 
    """
    edition = Edition(year = 2022)
    database_session.add(edition)
    database_session.commit()
    database_session.refresh(edition)

    # Make the delete request
    response = test_client.delete(f"/editions/{edition.edition_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Try to make a delete on an editions that doesn't exist
    response = test_client.delete("/edition/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND