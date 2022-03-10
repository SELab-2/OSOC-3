from json import dumps
from sqlalchemy.orm import Session
from starlette import status
from starlette.testclient import TestClient

from src.database.models import Edition

def test_get_editions(database_session: Session, test_client: TestClient):
    edition = Edition(year = 2022)
    database_session.add(edition)
    database_session.commit()

    response = test_client.get("/editions/")

    assert response.status_code == status.HTTP_200_OK
    json = response.json()


def test_create_edition(database_session: Session, test_client: TestClient):
    # Verify that editions doesn't exist yet
    assert test_client.get("/editions/1/").status_code == status.HTTP_404_NOT_FOUND

    # Make the post request
    response = test_client.post("/editions/1/", data=dumps({"year": "2022"}))
    assert response.status_code == status.HTTP_201_CREATED


    