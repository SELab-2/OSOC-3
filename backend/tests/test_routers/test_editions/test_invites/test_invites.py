from json import dumps
from uuid import UUID

from sqlalchemy.orm import Session
from starlette import status

from src.database.models import Edition, InviteLink
from tests.utils.authorization import AuthClient


def test_get_empty_invites(database_session: Session, auth_client: AuthClient):
    """Test endpoint for getting invites when db is empty"""
    auth_client.admin()
    database_session.add(Edition(year=2022))
    database_session.commit()

    response = auth_client.get("/editions/1/invites")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"inviteLinks": []}


def test_get_invites(database_session: Session, auth_client: AuthClient):
    """Test endpoint for getting invites when db is not empty"""
    auth_client.admin()
    edition = Edition(year=2022)
    database_session.add(edition)
    database_session.commit()
    database_session.add(InviteLink(target_email="test@ema.il", edition=edition))
    database_session.commit()

    response = auth_client.get("/editions/1/invites")

    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert len(json["inviteLinks"]) == 1
    link = json["inviteLinks"][0]
    assert link["id"] == 1
    assert link["email"] == "test@ema.il"
    assert link["editionId"] == 1


def test_create_invite_valid(database_session: Session, auth_client: AuthClient):
    """Test endpoint for creating invites when data is valid"""
    auth_client.admin()
    edition = Edition(year=2022)
    database_session.add(edition)
    database_session.commit()

    # Create POST request
    response = auth_client.post("/editions/1/invites/", data=dumps({"email": "test@ema.il"}))
    assert response.status_code == status.HTTP_201_CREATED
    json = response.json()
    assert "mailTo" in json
    assert json["mailTo"].startswith("mailto:test@ema.il")

    # New entry made in database
    json = auth_client.get("/editions/1/invites/").json()
    assert len(json["inviteLinks"]) == 1
    new_uuid = json["inviteLinks"][0]["uuid"]
    assert auth_client.get(f"/editions/1/invites/{new_uuid}/").status_code == status.HTTP_200_OK


def test_create_invite_invalid(database_session: Session, auth_client: AuthClient):
    """Test endpoint for creating invites when data is invalid"""
    auth_client.admin()
    edition = Edition(year=2022)
    database_session.add(edition)
    database_session.commit()

    # Invalid POST will send invalid status code
    response = auth_client.post("/editions/1/invites/", data=dumps({"email": "invalid field"}))
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # Verify that no new entry was made after the error
    assert len(auth_client.get("/editions/1/invites/").json()["inviteLinks"]) == 0


def test_delete_invite_invalid(database_session: Session, auth_client: AuthClient):
    """Test endpoint for deleting invites when uuid is malformed"""
    auth_client.admin()
    assert auth_client.delete("/editions/1/invites/1").status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_delete_invite_valid(database_session: Session, auth_client: AuthClient):
    """Test endpoint for deleting invites when uuid is valid"""
    auth_client.admin()
    edition = Edition(year=2022)
    database_session.add(edition)
    database_session.commit()

    debug_uuid = "123e4567-e89b-12d3-a456-426614174000"

    # Not present yet
    assert auth_client.delete(f"/editions/1/invites/{debug_uuid}").status_code == status.HTTP_404_NOT_FOUND

    # Create new entry in db
    invite_link = InviteLink(target_email="test@ema.il", edition=edition, uuid=UUID(debug_uuid))
    database_session.add(invite_link)
    database_session.commit()

    # Remove
    assert auth_client.delete(f"/editions/1/invites/{invite_link.uuid}").status_code == status.HTTP_204_NO_CONTENT

    # Not found anymore
    assert auth_client.get(f"/editions/1/invites/{invite_link.uuid}/").status_code == status.HTTP_404_NOT_FOUND


def test_get_invite_malformed_uuid(database_session: Session, auth_client: AuthClient):
    """Test endpoint for fetching invites when uuid is malformed"""
    auth_client.admin()
    edition = Edition(year=2022)
    database_session.add(edition)
    database_session.commit()

    # Verify malformed uuid (1)
    assert auth_client.get("/editions/1/invites/1/").status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_invite_non_existing(database_session: Session, auth_client: AuthClient):
    """Test endpoint for fetching invites when uuid is valid but doesn't exist"""
    auth_client.admin()
    edition = Edition(year=2022)
    database_session.add(edition)
    database_session.commit()

    assert auth_client.get(
        "/editions/1/invites/123e4567-e89b-12d3-a456-426614174000").status_code == status.HTTP_404_NOT_FOUND


def test_get_invite_present(database_session: Session, auth_client: AuthClient):
    """Test endpoint to fetch an invite when one is present"""
    auth_client.admin()
    edition = Edition(year=2022)
    database_session.add(edition)
    database_session.commit()

    debug_uuid = "123e4567-e89b-12d3-a456-426614174000"

    # Create new entry in db
    invite_link = InviteLink(target_email="test@ema.il", edition=edition, uuid=UUID(debug_uuid))
    database_session.add(invite_link)
    database_session.commit()

    # Found the correct result now
    response = auth_client.get(f"/editions/1/invites/{debug_uuid}")
    json = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert json["uuid"] == debug_uuid
    assert json["email"] == "test@ema.il"
