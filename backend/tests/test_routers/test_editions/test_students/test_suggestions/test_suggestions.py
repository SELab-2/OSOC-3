from sqlalchemy.orm import Session
from starlette import status
from starlette.testclient import TestClient
from tests.fill_database import fill_database
from src.database.models import Suggestion, Student, User
from src.app.utils.dependencies import get_current_active_user


def test_new_suggestion(database_session: Session, test_client: TestClient):
    fill_database(database_session)
    email = "coach1@noutlook.be"
    password = "wachtwoord"
    form = {
        "username": email,
        "password": password
    }
    d = test_client.post("/login/token", data=form).json()["accessToken"]
    auth = "Bearer "+d
    assert test_client.post("/editions/1/students/29/suggestions/", headers={"Authorization": auth}, json={"suggestion":1, "argumentation":"test"}).status_code == status.HTTP_201_CREATED
    suggestions: list[Suggestion] = database_session.query(Suggestion).where(Suggestion.student_id==29).all()
    assert len(suggestions) > 0

def test_new_suggestion_not_authorized(database_session: Session, test_client: TestClient):
    assert test_client.post("/editions/1/students/29/suggestions/", json={"suggestion":1, "argumentation":"test"}).status_code == status.HTTP_401_UNAUTHORIZED
    suggestions: list[Suggestion] = database_session.query(Suggestion).where(Suggestion.student_id==29).all()
    assert len(suggestions) == 0

def test_get_suggestions_of_student(database_session: Session, test_client: TestClient):
    fill_database(database_session)
    form = {
        "username": "coach1@noutlook.be",
        "password": "wachtwoord"
    }
    d = test_client.post("/login/token", data=form).json()["accessToken"]
    auth = "Bearer "+d
    assert test_client.post("/editions/1/students/29/suggestions/", headers={"Authorization": auth}, json={"suggestion":1, "argumentation":"test"}).status_code == status.HTTP_201_CREATED
    form = {
        "username": "admin@ngmail.com",
        "password": "wachtwoord"
    }
    d = test_client.post("/login/token", data=form).json()["accessToken"]
    auth = "Bearer "+d
    assert test_client.post("/editions/1/students/29/suggestions/", headers={"Authorization": auth}, json={"suggestion":1, "argumentation":"test"}).status_code == status.HTTP_201_CREATED
    

#, json={"suggestion":"OK", "argumentation":"test"}


"""
def test_ok(database_session: Session, test_client: TestClient):
    database_session.add(Edition(year=2022))
    database_session.commit()
    response = test_client.post("/editions/1/register/email", json={"name": "Joskes vermeulen","email": "jw@gmail.com", "pw": "test"})
    assert response.status_code == status.
"""