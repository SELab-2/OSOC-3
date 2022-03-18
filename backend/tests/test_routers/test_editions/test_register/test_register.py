from sqlalchemy.orm import Session
from starlette import status
from starlette.testclient import TestClient

from src.database.models import Edition

def test_ok(database_session: Session, test_client: TestClient):
    """Tests a registeration is made"""
    database_session.add(Edition(year=2022))
    database_session.commit()
    response = test_client.post("/editions/1/register/email", json={"name": "Joskes vermeulen","email": "jw@gmail.com", "pw": "test"})
    assert response.status_code == status.HTTP_201_CREATED

def test_no_edition(database_session: Session, test_client: TestClient):
    """Tests if there is no edition it gets the right error code"""
    response = test_client.post("/editions/1/register/email", json={"name": "Joskes vermeulen","email": "jw@gmail.com", "pw": "test"})
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_not_a_correct_email(database_session: Session, test_client: TestClient):
    """Tests when the email isn't correct, it gets the right error code"""
    database_session.add(Edition(year=2022))
    database_session.commit()
    response = test_client.post("/editions/1/register/email", json={"name": "Joskes vermeulen","email": "jw", "pw": "test"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_duplicate(database_session: Session, test_client: TestClient):
    """Tests when there is a duplicate, it gets the right error code"""
    database_session.add(Edition(year=2022))
    database_session.commit()
    test_client.post("/editions/1/register/email", json={"name": "Joskes vermeulen","email": "jw@gmail.com", "pw": "test"})
    response = test_client.post("/editions/1/register/email", json={"name": "Joske vermeulen","email": "jw@gmail.com", "pw": "test1"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST