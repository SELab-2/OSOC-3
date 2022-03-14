from json import dumps
from sqlalchemy.orm import Session
from starlette import status
from starlette.testclient import TestClient

from src.database.models import Edition

def test_ok(database_session: Session, test_client: TestClient):
    database_session.add(Edition(year=2022))
    database_session.commit()
    response = test_client.post("/editions/1/register/email", data=dumps({"name": "Joskes vermeulen","email": "jw@gmail.com", "pw": "test"}))
    assert response.status_code == status.HTTP_201_CREATED

'''
def test_get_empty_invites(database_session: Session, test_client: TestClient):
    database_session.add(Edition(year=2022))
    database_session.commit()

    response = test_client.get("/editions/1/invites")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"inviteLinks": []}


def test_get_invites(database_session: Session, test_client: TestClient):
    edition = Edition(year=2022)
    database_session.add(edition)
    database_session.commit()
    database_session.add(InviteLink(target_email="test@ema.il", edition=edition))
    database_session.commit()

    response = test_client.get("/editions/1/invites")

    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert len(json["inviteLinks"]) == 1
    link = json["inviteLinks"][0]
    assert link["id"] == 1
    assert link["email"] == "test@ema.il"
    assert link["editionId"] == 1


def test_create_invite(database_session: Session, test_client: TestClient):
    edition = Edition(year=2022)
    database_session.add(edition)
    database_session.commit()

    # Verify that entity doesn't exist
    assert test_client.get("/editions/1/invites/1/").status_code == status.HTTP_404_NOT_FOUND

    # Create POST request
    response = test_client.post("/editions/1/invites/", data=dumps({"email": "test@ema.il"}))
    assert response.status_code == status.HTTP_201_CREATED
    json: dict[str, str] = response.json()
    assert "mailTo" in json
    assert json["mailTo"].startswith("mailto:test@ema.il")

    # New entry made in database
    assert len(test_client.get("/editions/1/invites/").json()["inviteLinks"]) == 1
    assert test_client.get("/editions/1/invites/1/").status_code == status.HTTP_200_OK

    # Invalid POST will send invalid status code
    response = test_client.post("/editions/1/invites/", data=dumps({"email": "invalid field"}))
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # Verify that no new entry was made after the error
    assert len(test_client.get("/editions/1/invites/").json()["inviteLinks"]) == 1


def test_delete_invite(database_session: Session, test_client: TestClient):
    edition = Edition(year=2022)
    database_session.add(edition)
    database_session.commit()

    # Not present yet
    assert test_client.delete("/editions/1/invites/1").status_code == status.HTTP_404_NOT_FOUND

    # Create new entry in db
    invite_link = InviteLink(target_email="test@ema.il", edition=edition)
    database_session.add(invite_link)
    database_session.commit()

    # Remove
    assert test_client.delete("/editions/1/invites/1").status_code == status.HTTP_204_NO_CONTENT

    # Not found anymore
    assert test_client.get("/editions/1/invites/1/").status_code == status.HTTP_404_NOT_FOUND


def test_get_invite(database_session: Session, test_client: TestClient):
    edition = Edition(year=2022)
    database_session.add(edition)
    database_session.commit()

    # Not present yet
    assert test_client.get("/editions/1/invites/1").status_code == status.HTTP_404_NOT_FOUND

    # Create new entry in db
    invite_link = InviteLink(target_email="test@ema.il", edition=edition)
    database_session.add(invite_link)
    database_session.commit()

    # Found the correct result now
    response = test_client.get("/editions/1/invites/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == 1
    assert response.json()["email"] == "test@ema.il"
'''