from sqlalchemy.orm import Session
from starlette import status
from starlette.testclient import TestClient

from src.database.models import Edition

def test_ok(database_session: Session, test_client: TestClient):
    database_session.add(Edition(year=2022))
    database_session.commit()
    response = test_client.post("/editions/1/register/email", json={"name": "Joskes vermeulen","email": "jw@gmail.com", "pw": "test"})
    assert response.status_code == status.HTTP_201_CREATED

def test_no_edition(database_session: Session, test_client: TestClient):
    response = test_client.post("/editions/1/register/email", json={"name": "Joskes vermeulen","email": "jw@gmail.com", "pw": "test"})
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_duplicate(database_session: Session, test_client: TestClient):
    database_session.add(Edition(year=2022))
    database_session.commit()
    test_client.post("/editions/1/register/email", json={"name": "Joskes vermeulen","email": "jw@gmail.com", "pw": "test"})
    response = test_client.post("/editions/1/register/email", json={"name": "Joske vermeulen","email": "jw@gmail.com", "pw": "test1"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST