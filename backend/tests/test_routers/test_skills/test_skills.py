from json import dumps
from sqlalchemy.orm import Session
from starlette import status
from starlette.testclient import TestClient

from src.database.models import Skill


def test_get_skills(database_session: Session, test_client: TestClient):
    """Performe tests on getting skills

    Args:
        database_session (Session): a connection with the database
        test_client (TestClient): a client used to do rest calls 
    """
    skill = Skill(name="Backend", description = "Must know react")
    database_session.add(skill)
    database_session.commit()

    # Make the get request
    response = test_client.get("/skills/")

    assert response.status_code == status.HTTP_200_OK
    response = response.json()
    assert response["skills"][0]["name"] == "Backend"
    assert response["skills"][0]["description"] == "Must know react"


def test_create_skill(database_session: Session, test_client: TestClient):
    """Performe tests on creating skills

    Args:
        database_session (Session): a connection with the database
        test_client (TestClient): a client used to do rest calls 
    """
    # Make the post request
    response = test_client.post("/skills/", data=dumps({"name": "Backend", "description": "must know react"}))
    assert response.status_code == status.HTTP_201_CREATED
    assert test_client.get("/skills/").json()["skills"][0]["name"] == "Backend"
    assert test_client.get("/skills/").json()["skills"][0]["description"] == "must know react"


def test_delete_skill(database_session: Session, test_client: TestClient):
    """Performe tests on deleting skills

    Args:
        database_session (Session): a connection with the database
        test_client (TestClient): a client used to do rest calls 
    """
    skill = Skill(name="Backend", description = "Must know react")
    database_session.add(skill)
    database_session.commit()
    database_session.refresh(skill)

    response = test_client.delete(f"/skills/{skill.skill_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Try to make a delete on an editions that doesn't exist
    response = test_client.delete("/skills/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND