from sqlalchemy.orm import Session
from starlette import status
from starlette.testclient import TestClient
from tests.fill_database import fill_database
from src.database.models import Suggestion, Student, User


def test_new_suggestion(database_session: Session, test_client: TestClient):
    """Tests a new sugesstion"""

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
    """Tests when not authorized you can't add a new suggestion"""

    fill_database(database_session)
    assert test_client.post("/editions/1/students/29/suggestions/", json={"suggestion":1, "argumentation":"test"}).status_code == status.HTTP_401_UNAUTHORIZED
    suggestions: list[Suggestion] = database_session.query(Suggestion).where(Suggestion.student_id==29).all()
    assert len(suggestions) == 0


def test_get_suggestions_of_student_not_authorized(database_session: Session, test_client: TestClient):
    """Tests if you don't have the right access, you get the right HTTP code"""

    assert test_client.get("/editions/1/students/29/suggestions/", headers={"Authorization": "auth"}, json={"suggestion":1, "argumentation":"Ja"}).status_code == status.HTTP_401_UNAUTHORIZED


def test_get_suggestions_of_ghost(database_session: Session, test_client: TestClient):
    """Tests if the student don't exist, you get a 404"""

    fill_database(database_session)
    email = "coach1@noutlook.be"
    password = "wachtwoord"
    form = {
        "username": email,
        "password": password
    }
    d = test_client.post("/login/token", data=form).json()["accessToken"]
    auth = "Bearer "+d
    res = test_client.get("/editions/1/students/9000/suggestions/", headers={"Authorization": auth})
    assert res.status_code == status.HTTP_404_NOT_FOUND
    

def test_get_suggestions_of_student(database_session: Session, test_client: TestClient):
    """Tests to get the suggestions of a student"""

    fill_database(database_session)
    form = {
        "username": "coach1@noutlook.be",
        "password": "wachtwoord"
    }
    d = test_client.post("/login/token", data=form).json()["accessToken"]
    auth = "Bearer "+d
    assert test_client.post("/editions/1/students/29/suggestions/", headers={"Authorization": auth}, json={"suggestion":1, "argumentation":"Ja"}).status_code == status.HTTP_201_CREATED
    form = {
        "username": "admin@ngmail.com",
        "password": "wachtwoord"
    }
    d = test_client.post("/login/token", data=form).json()["accessToken"]
    auth = "Bearer "+d
    assert test_client.post("/editions/1/students/29/suggestions/", headers={"Authorization": auth}, json={"suggestion":3, "argumentation":"Neen"}).status_code == status.HTTP_201_CREATED
    res = test_client.get("/editions/1/students/29/suggestions/", headers={"Authorization": auth})
    assert res.status_code == status.HTTP_200_OK
    res_json = res.json()
    assert len(res_json["suggestions"]) == 2
    assert res_json["suggestions"][0]["coach"]["email"] == "coach1@noutlook.be"
    assert res_json["suggestions"][0]["suggestion"] == 1
    assert res_json["suggestions"][0]["argumentation"] == "Ja"
    assert res_json["suggestions"][1]["coach"]["email"] == "admin@ngmail.com"
    assert res_json["suggestions"][1]["suggestion"] == 3
    assert res_json["suggestions"][1]["argumentation"] == "Neen"

def test_delete_ghost_suggestion(database_session: Session, test_client: TestClient):
    fill_database(database_session)
    form = {
        "username": "admin@ngmail.com",
        "password": "wachtwoord"
    }
    d = test_client.post("/login/token", data=form).json()["accessToken"]
    auth = "Bearer "+d
    assert test_client.delete("/editions/1/students/1/suggestions/8000", headers={"Authorization": auth}).status_code == status.HTTP_404_NOT_FOUND

def test_delete_not_autorized(database_session: Session, test_client: TestClient):
    fill_database(database_session)
    assert test_client.delete("/editions/1/students/1/suggestions/8000", headers={"Authorization": "auth"}).status_code == status.HTTP_401_UNAUTHORIZED

def test_delete_suggestion_admin(database_session: Session, test_client: TestClient):
    fill_database(database_session)
    form = {
        "username": "admin@ngmail.com",
        "password": "wachtwoord"
    }
    d = test_client.post("/login/token", data=form).json()["accessToken"]
    auth = "Bearer "+d
    assert test_client.delete("/editions/1/students/1/suggestions/1", headers={"Authorization": auth}).status_code == status.HTTP_204_NO_CONTENT
    suggestions: Suggestion = database_session.query(Suggestion).where(Suggestion.suggestion_id==1).all()
    assert len(suggestions) == 0
