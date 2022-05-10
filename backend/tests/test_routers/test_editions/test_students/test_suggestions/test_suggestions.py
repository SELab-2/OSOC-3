import pytest
from sqlalchemy.orm import Session
from starlette import status
from src.database.enums import DecisionEnum
from src.database.models import Suggestion, Student, User, Edition, Skill

from tests.utils.authorization import AuthClient


@pytest.fixture
def database_with_data(database_session: Session) -> Session:
    """A fixture to fill the database with fake data that can easly be used when testing"""

    # Editions
    edition: Edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    database_session.commit()

    # Users
    coach1: User = User(name="coach1", editions=[edition])
    database_session.add(coach1)
    database_session.commit()

    # Skill
    skill1: Skill = Skill(name="skill1", description="something about skill1")
    skill2: Skill = Skill(name="skill2", description="something about skill2")
    skill3: Skill = Skill(name="skill3", description="something about skill3")
    skill4: Skill = Skill(name="skill4", description="something about skill4")
    skill5: Skill = Skill(name="skill5", description="something about skill5")
    skill6: Skill = Skill(name="skill6", description="something about skill6")
    database_session.add(skill1)
    database_session.add(skill2)
    database_session.add(skill3)
    database_session.add(skill4)
    database_session.add(skill5)
    database_session.add(skill6)
    database_session.commit()

    # Student
    student01: Student = Student(first_name="Jos", last_name="Vermeulen", preferred_name="Joske",
                                 email_address="josvermeulen@mail.com", phone_number="0487/86.24.45", alumni=True,
                                 wants_to_be_student_coach=True, edition=edition, skills=[skill1, skill3, skill6])
    student30: Student = Student(first_name="Marta", last_name="Marquez", preferred_name="Marta",
                                 email_address="marta.marquez@example.com", phone_number="967-895-285", alumni=True,
                                 wants_to_be_student_coach=False, edition=edition, skills=[skill2, skill4, skill5])

    database_session.add(student01)
    database_session.add(student30)
    database_session.commit()

    # Suggestion
    suggestion1: Suggestion = Suggestion(
        student=student01, coach=coach1, argumentation="Good student", suggestion=DecisionEnum.YES)
    database_session.add(suggestion1)
    database_session.commit()
    return database_session


def test_new_suggestion(database_with_data: Session, auth_client: AuthClient):
    """Tests creating a new suggestion"""
    edition: Edition = database_with_data.query(Edition).all()[0]
    auth_client.coach(edition)
    resp = auth_client.post("/editions/ed2022/students/2/suggestions",
                            json={"suggestion": 1, "argumentation": "test"})
    assert resp.status_code == status.HTTP_201_CREATED
    suggestions: list[Suggestion] = database_with_data.query(
        Suggestion).where(Suggestion.student_id == 2).all()
    assert len(suggestions) == 1
    assert DecisionEnum(resp.json()["suggestion"]
                        ["suggestion"]) == suggestions[0].suggestion
    assert resp.json()[
        "suggestion"]["argumentation"] == suggestions[0].argumentation


def test_overwrite_suggestion(database_with_data: Session, auth_client: AuthClient):
    """Tests that when you've already made a suggestion earlier, the existing one is replaced"""
    # Create initial suggestion
    edition: Edition = database_with_data.query(Edition).all()[0]
    auth_client.coach(edition)
    auth_client.post("/editions/ed2022/students/2/suggestions",
                     json={"suggestion": 1, "argumentation": "test"})

    suggestions: list[Suggestion] = database_with_data.query(
        Suggestion).where(Suggestion.student_id == 2).all()
    assert len(suggestions) == 1

    # Send a new request
    arg = "overwritten"
    resp = auth_client.post("/editions/ed2022/students/2/suggestions",
                            json={"suggestion": 2, "argumentation": arg})
    assert resp.status_code == status.HTTP_201_CREATED
    suggestions: list[Suggestion] = database_with_data.query(
        Suggestion).where(Suggestion.student_id == 2).all()
    assert len(suggestions) == 1
    assert suggestions[0].argumentation == arg


def test_new_suggestion_not_authorized(database_with_data: Session, auth_client: AuthClient):
    """Tests when not authorized you can't add a new suggestion"""

    assert auth_client.post("/editions/ed2022/students/2/suggestions", json={
                            "suggestion": 1, "argumentation": "test"}).status_code == status.HTTP_401_UNAUTHORIZED
    suggestions: list[Suggestion] = database_with_data.query(
        Suggestion).where(Suggestion.student_id == 2).all()
    assert len(suggestions) == 0


def test_get_suggestions_of_student_not_authorized(database_with_data: Session, auth_client: AuthClient):
    """Tests if you don't have the right access, you get the right HTTP code"""

    assert auth_client.get("/editions/ed2022/students/29/suggestions", headers={"Authorization": "auth"}, json={
                           "suggestion": 1, "argumentation": "Ja"}).status_code == status.HTTP_401_UNAUTHORIZED


def test_get_suggestions_of_ghost(database_with_data: Session, auth_client: AuthClient):
    """Tests if the student don't exist, you get a 404"""
    edition: Edition = database_with_data.query(Edition).all()[0]
    auth_client.coach(edition)
    res = auth_client.get(
        "/editions/ed2022/students/9000/suggestions")
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_get_suggestions_of_student(database_with_data: Session, auth_client: AuthClient):
    """Tests to get the suggestions of a student"""
    edition: Edition = database_with_data.query(Edition).all()[0]
    auth_client.coach(edition)
    assert auth_client.post("/editions/ed2022/students/2/suggestions", json={
                            "suggestion": 1, "argumentation": "Ja"}).status_code == status.HTTP_201_CREATED
    auth_client.admin()
    assert auth_client.post("/editions/ed2022/students/2/suggestions", json={
                            "suggestion": 3, "argumentation": "Neen"}).status_code == status.HTTP_201_CREATED
    res = auth_client.get(
        "/editions/1/students/2/suggestions")
    assert res.status_code == status.HTTP_200_OK
    res_json = res.json()
    assert len(res_json["suggestions"]) == 2
    assert res_json["suggestions"][0]["suggestion"] == 1
    assert res_json["suggestions"][0]["argumentation"] == "Ja"
    assert res_json["suggestions"][1]["suggestion"] == 3
    assert res_json["suggestions"][1]["argumentation"] == "Neen"


def test_delete_ghost_suggestion(database_with_data: Session, auth_client: AuthClient):
    """Tests that you get the correct status code when you delete a not existing suggestion"""
    edition: Edition = database_with_data.query(Edition).all()[0]
    auth_client.coach(edition)
    assert auth_client.delete(
        "/editions/ed2022/students/1/suggestions/8000").status_code == status.HTTP_404_NOT_FOUND


def test_delete_not_autorized(database_with_data: Session, auth_client: AuthClient):
    """Tests that you have to be loged in for deleating a suggestion"""
    assert auth_client.delete(
        "/editions/ed2022/students/1/suggestions/8000").status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_suggestion_admin(database_with_data: Session, auth_client: AuthClient):
    """Test that an admin can update suggestions"""
    auth_client.admin()
    assert auth_client.delete(
        "/editions/ed2022/students/1/suggestions/1").status_code == status.HTTP_204_NO_CONTENT
    suggestions: Suggestion = database_with_data.query(
        Suggestion).where(Suggestion.suggestion_id == 1).all()
    assert len(suggestions) == 0


def test_delete_suggestion_coach_their_review(database_with_data: Session, auth_client: AuthClient):
    """Tests that a coach can delete their own suggestion"""
    edition: Edition = database_with_data.query(Edition).all()[0]
    auth_client.coach(edition)
    new_suggestion = auth_client.post("/editions/ed2022/students/2/suggestions",
                                      json={"suggestion": 1, "argumentation": "test"})
    assert new_suggestion.status_code == status.HTTP_201_CREATED
    suggestion_id = new_suggestion.json()["suggestion"]["suggestionId"]
    assert auth_client.delete(
        f"/editions/ed2022/students/1/suggestions/{suggestion_id}").status_code == status.HTTP_204_NO_CONTENT
    suggestions: Suggestion = database_with_data.query(
        Suggestion).where(Suggestion.suggestion_id == suggestion_id).all()
    assert len(suggestions) == 0


def test_delete_suggestion_coach_other_review(database_with_data: Session, auth_client: AuthClient):
    """Tests that a coach can't delete other coaches their suggestions"""
    edition: Edition = database_with_data.query(Edition).all()[0]
    auth_client.coach(edition)
    assert auth_client.delete(
        "/editions/ed2022/students/1/suggestions/1").status_code == status.HTTP_403_FORBIDDEN
    suggestions: Suggestion = database_with_data.query(
        Suggestion).where(Suggestion.suggestion_id == 1).all()
    assert len(suggestions) == 1


def test_update_ghost_suggestion(database_with_data: Session, auth_client: AuthClient):
    """Tests a suggestion that don't exist """
    auth_client.admin()
    assert auth_client.put("/editions/ed2022/students/1/suggestions/8000", json={
                           "suggestion": 1, "argumentation": "test"}).status_code == status.HTTP_404_NOT_FOUND


def test_update_not_autorized(database_with_data: Session, auth_client: AuthClient):
    """Tests update when not autorized"""
    assert auth_client.put("/editions/ed2022/students/1/suggestions/8000", json={
                           "suggestion": 1, "argumentation": "test"}).status_code == status.HTTP_401_UNAUTHORIZED


def test_update_suggestion_admin(database_with_data: Session, auth_client: AuthClient):
    """Test that an admin can update suggestions"""
    auth_client.admin()
    assert auth_client.put("/editions/ed2022/students/1/suggestions/1", json={
                           "suggestion": 3, "argumentation": "test"}).status_code == status.HTTP_204_NO_CONTENT
    suggestion: Suggestion = database_with_data.query(
        Suggestion).where(Suggestion.suggestion_id == 1).one()
    assert suggestion.suggestion == DecisionEnum.NO
    assert suggestion.argumentation == "test"


def test_update_suggestion_coach_their_review(database_with_data: Session, auth_client: AuthClient):
    """Tests that a coach can update their own suggestion"""
    edition: Edition = database_with_data.query(Edition).all()[0]
    auth_client.coach(edition)
    new_suggestion = auth_client.post("/editions/ed2022/students/2/suggestions",
                                      json={"suggestion": 1, "argumentation": "test"})
    assert new_suggestion.status_code == status.HTTP_201_CREATED
    suggestion_id = new_suggestion.json()["suggestion"]["suggestionId"]
    assert auth_client.put(f"/editions/ed2022/students/1/suggestions/{suggestion_id}", json={
                           "suggestion": 3, "argumentation": "test"}).status_code == status.HTTP_204_NO_CONTENT
    suggestion: Suggestion = database_with_data.query(
        Suggestion).where(Suggestion.suggestion_id == suggestion_id).one()
    assert suggestion.suggestion == DecisionEnum.NO
    assert suggestion.argumentation == "test"


def test_update_suggestion_coach_other_review(database_with_data: Session, auth_client: AuthClient):
    """Tests that a coach can't update other coaches their suggestions"""
    edition: Edition = database_with_data.query(Edition).all()[0]
    auth_client.coach(edition)
    assert auth_client.put("/editions/ed2022/students/1/suggestions/1", json={
                           "suggestion": 3, "argumentation": "test"}).status_code == status.HTTP_403_FORBIDDEN
    suggestion: Suggestion = database_with_data.query(
        Suggestion).where(Suggestion.suggestion_id == 1).one()
    assert suggestion.suggestion != DecisionEnum.NO
    assert suggestion.argumentation != "test"
