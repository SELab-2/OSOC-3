from json import dumps
from sqlalchemy.orm import Session
from starlette import status

from src.database.models import Skill
from tests.utils.authorization import AuthClient


def test_get_skills(database_session: Session, auth_client: AuthClient):
    """Performe tests on getting skills

    Args:
        database_session (Session): a connection with the database
        auth_client (AuthClient): a client used to do rest calls
    """
    auth_client.admin()
    skill = Skill(name="Backend", description="Must know react")
    database_session.add(skill)
    database_session.commit()

    # Make the get request
    response = auth_client.get("/skills/")

    assert response.status_code == status.HTTP_200_OK
    response = response.json()
    assert response["skills"][0]["name"] == "Backend"
    assert response["skills"][0]["description"] == "Must know react"


def test_create_skill(database_session: Session, auth_client: AuthClient):
    """Performe tests on creating skills

    Args:
        database_session (Session): a connection with the database
        auth_client (AuthClient): a client used to do rest calls
    """
    auth_client.admin()

    # Make the post request
    response = auth_client.post("/skills", data=dumps({"name": "Backend", "description": "must know react"}))
    assert response.status_code == status.HTTP_201_CREATED
    assert auth_client.get("/skills/").json()["skills"][0]["name"] == "Backend"
    assert auth_client.get("/skills/").json()["skills"][0]["description"] == "must know react"


def test_delete_skill(database_session: Session, auth_client: AuthClient):
    """Performe tests on deleting skills

    Args:
        database_session (Session): a connection with the database
        auth_client (AuthClient): a client used to do rest calls
    """
    auth_client.admin()

    skill = Skill(name="Backend", description="Must know react")
    database_session.add(skill)
    database_session.commit()
    database_session.refresh(skill)

    response = auth_client.delete(f"/skills/{skill.skill_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_skill_non_existing(database_session: Session, auth_client: AuthClient):
    """Delete a skill that doesn't exist"""
    auth_client.admin()

    response = auth_client.delete("/skills/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND
