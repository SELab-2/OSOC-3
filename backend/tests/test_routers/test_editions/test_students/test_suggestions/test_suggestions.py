from sqlalchemy.orm import Session
from starlette import status
from starlette.testclient import TestClient
from src.database.enums import DecisionEnum
from src.database.models import Suggestion, Student, User, Edition, Skill, AuthEmail
from src.app.logic.security import get_password_hash


def fill_database(db):
    """A function to fill the database with fake data that can easly be used when testing"""
    # Editions
    edition: Edition = Edition(year=2022)
    db.add(edition)
    db.commit()

    # Users
    admin: User = User(name="admin", email="admin@ngmail.com", admin=True)
    coach1: User = User(name="coach1", email="coach1@noutlook.be")
    coach2: User = User(name="coach2", email="coach2@noutlook.be")
    request: User = User(name="request", email="request@ngmail.com")
    db.add(admin)
    db.add(coach1)
    db.add(coach2)
    db.add(request)
    db.commit()

    # AuthEmail
    pw_hash = get_password_hash("wachtwoord")
    auth_email_admin: AuthEmail = AuthEmail(user=admin, pw_hash=pw_hash)
    auth_email_coach1: AuthEmail = AuthEmail(user=coach1, pw_hash=pw_hash)
    auth_email_coach2: AuthEmail = AuthEmail(user=coach2, pw_hash=pw_hash)
    auth_email_request: AuthEmail = AuthEmail(user=request, pw_hash=pw_hash)
    db.add(auth_email_admin)
    db.add(auth_email_coach1)
    db.add(auth_email_coach2)
    db.add(auth_email_request)
    db.commit()

    # Skill
    skill1: Skill = Skill(name="skill1", description="something about skill1")
    skill2: Skill = Skill(name="skill2", description="something about skill2")
    skill3: Skill = Skill(name="skill3", description="something about skill3")
    skill4: Skill = Skill(name="skill4", description="something about skill4")
    skill5: Skill = Skill(name="skill5", description="something about skill5")
    skill6: Skill = Skill(name="skill6", description="something about skill6")
    db.add(skill1)
    db.add(skill2)
    db.add(skill3)
    db.add(skill4)
    db.add(skill5)
    db.add(skill6)
    db.commit()

    # Student
    student01: Student = Student(first_name="Jos", last_name="Vermeulen", preferred_name="Joske",
                                 email_address="josvermeulen@mail.com", phone_number="0487/86.24.45", alumni=True,
                                 wants_to_be_student_coach=True, edition=edition, skills=[skill1, skill3, skill6])
    student30: Student = Student(first_name="Marta", last_name="Marquez", preferred_name="Marta",
                                 email_address="marta.marquez@example.com", phone_number="967-895-285", alumni=True,
                                 wants_to_be_student_coach=False, edition=edition, skills=[skill2, skill4, skill5])

    db.add(student01)
    db.add(student30)
    db.commit()

    # Suggestion
    suggestion1: Suggestion = Suggestion(
        student=student01, coach=coach1, argumentation="Good student", suggestion=DecisionEnum.YES)
    db.add(suggestion1)
    db.commit()


def test_new_suggestion(database_session: Session, test_client: TestClient):
    """Tests a new sugesstion"""

    fill_database(database_session)
    email = "coach1@noutlook.be"
    password = "wachtwoord"
    form = {
        "username": email,
        "password": password
    }
    token = test_client.post("/login/token", data=form).json()["accessToken"]
    auth = "Bearer " + token
    resp = test_client.post("/editions/1/students/2/suggestions/", headers={
                            "Authorization": auth}, json={"suggestion": 1, "argumentation": "test"})
    assert resp.status_code == status.HTTP_201_CREATED
    suggestions: list[Suggestion] = database_session.query(
        Suggestion).where(Suggestion.student_id == 2).all()
    assert len(suggestions) == 1
    print(resp.json())
    assert resp.json()[
        "suggestion"]["coach"]["email"] == suggestions[0].coach.email
    assert DecisionEnum(resp.json()["suggestion"]
                        ["suggestion"]) == suggestions[0].suggestion
    assert resp.json()[
        "suggestion"]["argumentation"] == suggestions[0].argumentation


def test_new_suggestion_not_authorized(database_session: Session, test_client: TestClient):
    """Tests when not authorized you can't add a new suggestion"""

    fill_database(database_session)
    assert test_client.post("/editions/1/students/2/suggestions/", json={
                            "suggestion": 1, "argumentation": "test"}).status_code == status.HTTP_401_UNAUTHORIZED
    suggestions: list[Suggestion] = database_session.query(
        Suggestion).where(Suggestion.student_id == 29).all()
    assert len(suggestions) == 0


def test_get_suggestions_of_student_not_authorized(database_session: Session, test_client: TestClient):
    """Tests if you don't have the right access, you get the right HTTP code"""

    assert test_client.get("/editions/1/students/29/suggestions/", headers={"Authorization": "auth"}, json={
                           "suggestion": 1, "argumentation": "Ja"}).status_code == status.HTTP_401_UNAUTHORIZED


def test_get_suggestions_of_ghost(database_session: Session, test_client: TestClient):
    """Tests if the student don't exist, you get a 404"""

    fill_database(database_session)
    email = "coach1@noutlook.be"
    password = "wachtwoord"
    form = {
        "username": email,
        "password": password
    }
    token = test_client.post("/login/token", data=form).json()["accessToken"]
    auth = "Bearer " + token
    res = test_client.get(
        "/editions/1/students/9000/suggestions/", headers={"Authorization": auth})
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_get_suggestions_of_student(database_session: Session, test_client: TestClient):
    """Tests to get the suggestions of a student"""

    fill_database(database_session)
    form = {
        "username": "coach1@noutlook.be",
        "password": "wachtwoord"
    }
    token = test_client.post("/login/token", data=form).json()["accessToken"]
    auth = "Bearer " + token
    assert test_client.post("/editions/1/students/2/suggestions/", headers={"Authorization": auth}, json={
                            "suggestion": 1, "argumentation": "Ja"}).status_code == status.HTTP_201_CREATED
    form = {
        "username": "admin@ngmail.com",
        "password": "wachtwoord"
    }
    token = test_client.post("/login/token", data=form).json()["accessToken"]
    auth = "Bearer " + token
    assert test_client.post("/editions/1/students/2/suggestions/", headers={"Authorization": auth}, json={
                            "suggestion": 3, "argumentation": "Neen"}).status_code == status.HTTP_201_CREATED
    res = test_client.get(
        "/editions/1/students/2/suggestions/", headers={"Authorization": auth})
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
    """Tests that you get the correct status code when you delete a not existing suggestion"""
    fill_database(database_session)
    form = {
        "username": "admin@ngmail.com",
        "password": "wachtwoord"
    }
    token = test_client.post("/login/token", data=form).json()["accessToken"]
    auth = "Bearer " + token
    assert test_client.delete("/editions/1/students/1/suggestions/8000", headers={
                              "Authorization": auth}).status_code == status.HTTP_404_NOT_FOUND


def test_delete_not_autorized(database_session: Session, test_client: TestClient):
    """Tests that you have to be loged in for deleating a suggestion"""
    fill_database(database_session)
    assert test_client.delete("/editions/1/students/1/suggestions/8000", headers={
                              "Authorization": "auth"}).status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_suggestion_admin(database_session: Session, test_client: TestClient):
    """Test that an admin can update suggestions"""
    fill_database(database_session)
    form = {
        "username": "admin@ngmail.com",
        "password": "wachtwoord"
    }
    token = test_client.post("/login/token", data=form).json()["accessToken"]
    auth = "Bearer " + token
    assert test_client.delete("/editions/1/students/1/suggestions/1", headers={
                              "Authorization": auth}).status_code == status.HTTP_204_NO_CONTENT
    suggestions: Suggestion = database_session.query(
        Suggestion).where(Suggestion.suggestion_id == 1).all()
    assert len(suggestions) == 0


def test_delete_suggestion_coach_their_review(database_session: Session, test_client: TestClient):
    """Tests that a coach can delete their own suggestion"""
    fill_database(database_session)
    form = {
        "username": "coach1@noutlook.be",
        "password": "wachtwoord"
    }
    token = test_client.post("/login/token", data=form).json()["accessToken"]
    auth = "Bearer " + token
    assert test_client.delete("/editions/1/students/1/suggestions/1", headers={
                              "Authorization": auth}).status_code == status.HTTP_204_NO_CONTENT
    suggestions: Suggestion = database_session.query(
        Suggestion).where(Suggestion.suggestion_id == 1).all()
    assert len(suggestions) == 0


def test_delete_suggestion_coach_other_review(database_session: Session, test_client: TestClient):
    """Tests that a coach can't delete other coaches their suggestions"""
    fill_database(database_session)
    form = {
        "username": "coach2@noutlook.be",
        "password": "wachtwoord"
    }
    token = test_client.post("/login/token", data=form).json()["accessToken"]
    auth = "Bearer " + token
    assert test_client.delete("/editions/1/students/1/suggestions/1", headers={
                              "Authorization": auth}).status_code == status.HTTP_403_FORBIDDEN
    suggestions: Suggestion = database_session.query(
        Suggestion).where(Suggestion.suggestion_id == 1).all()
    assert len(suggestions) == 1


def test_update_ghost_suggestion(database_session: Session, test_client: TestClient):
    """Tests a suggestion that don't exist """
    fill_database(database_session)
    form = {
        "username": "admin@ngmail.com",
        "password": "wachtwoord"
    }
    token = test_client.post("/login/token", data=form).json()["accessToken"]
    auth = "Bearer " + token
    assert test_client.put("/editions/1/students/1/suggestions/8000", headers={"Authorization": auth}, json={
                           "suggestion": 1, "argumentation": "test"}).status_code == status.HTTP_404_NOT_FOUND


def test_update_not_autorized(database_session: Session, test_client: TestClient):
    """Tests update when not autorized"""
    fill_database(database_session)
    assert test_client.put("/editions/1/students/1/suggestions/8000", headers={"Authorization": "auth"}, json={
                           "suggestion": 1, "argumentation": "test"}).status_code == status.HTTP_401_UNAUTHORIZED


def test_update_suggestion_admin(database_session: Session, test_client: TestClient):
    """Test that an admin can update suggestions"""
    fill_database(database_session)
    form = {
        "username": "admin@ngmail.com",
        "password": "wachtwoord"
    }
    token = test_client.post("/login/token", data=form).json()["accessToken"]
    auth = "Bearer " + token
    assert test_client.put("/editions/1/students/1/suggestions/1", headers={"Authorization": auth}, json={
                           "suggestion": 3, "argumentation": "test"}).status_code == status.HTTP_204_NO_CONTENT
    suggestion: Suggestion = database_session.query(
        Suggestion).where(Suggestion.suggestion_id == 1).one()
    assert suggestion.suggestion == DecisionEnum.NO
    assert suggestion.argumentation == "test"


def test_update_suggestion_coach_their_review(database_session: Session, test_client: TestClient):
    """Tests that a coach can update their own suggestion"""
    fill_database(database_session)
    form = {
        "username": "coach1@noutlook.be",
        "password": "wachtwoord"
    }
    token = test_client.post("/login/token", data=form).json()["accessToken"]
    auth = "Bearer " + token
    assert test_client.put("/editions/1/students/1/suggestions/1", headers={"Authorization": auth}, json={
                           "suggestion": 3, "argumentation": "test"}).status_code == status.HTTP_204_NO_CONTENT
    suggestion: Suggestion = database_session.query(
        Suggestion).where(Suggestion.suggestion_id == 1).one()
    assert suggestion.suggestion == DecisionEnum.NO
    assert suggestion.argumentation == "test"


def test_update_suggestion_coach_other_review(database_session: Session, test_client: TestClient):
    """Tests that a coach can't update other coaches their suggestions"""
    fill_database(database_session)
    form = {
        "username": "coach2@noutlook.be",
        "password": "wachtwoord"
    }
    token = test_client.post("/login/token", data=form).json()["accessToken"]
    auth = "Bearer " + token
    assert test_client.put("/editions/1/students/1/suggestions/1", headers={"Authorization": auth}, json={
                           "suggestion": 3, "argumentation": "test"}).status_code == status.HTTP_403_FORBIDDEN
    suggestion: Suggestion = database_session.query(
        Suggestion).where(Suggestion.suggestion_id == 1).one()
    assert suggestion.suggestion != DecisionEnum.NO
    assert suggestion.argumentation != "test"
