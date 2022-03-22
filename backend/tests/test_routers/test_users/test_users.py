from json import dumps

import pytest
from sqlalchemy.orm import Session

from starlette.testclient import TestClient
from starlette import status

from src.database import models
from src.database.models import user_editions, CoachRequest
from tests.utils.authorization import AuthClient


@pytest.fixture
def data(database_session: Session) -> dict[str, str | int]:
    """Fill database with dummy data"""
    # Create users
    user1 = models.User(name="user1", email="user1@mail.com", admin=True)

    database_session.add(user1)
    user2 = models.User(name="user2", email="user2@mail.com", admin=False)
    database_session.add(user2)

    # Create editions
    edition1 = models.Edition(year=1)
    database_session.add(edition1)
    edition2 = models.Edition(year=2)
    database_session.add(edition2)

    database_session.commit()

    # Create coach roles
    database_session.execute(models.user_editions.insert(), [
        {"user_id": user1.user_id, "edition_id": edition1.edition_id},
        {"user_id": user2.user_id, "edition_id": edition1.edition_id},
        {"user_id": user2.user_id, "edition_id": edition2.edition_id}
    ])

    return {"user1": user1.user_id,
            "user2": user2.user_id,
            "edition1": edition1.edition_id,
            "edition2": edition2.edition_id,
            }


def test_get_all_users(database_session: Session, auth_client: AuthClient, data: dict[str, str | int]):
    """Test endpoint for getting a list of users"""
    auth_client.admin()
    # All users
    response = auth_client.get("/users")
    assert response.status_code == status.HTTP_200_OK
    user_ids = [user["userId"] for user in response.json()['users']]
    user_ids.remove(auth_client.user.user_id)
    assert len(user_ids) == 2
    assert data["user1"] in user_ids
    assert data["user2"] in user_ids


def test_get_all_admins(database_session: Session, auth_client: AuthClient, data: dict[str, str | int]):
    """Test endpoint for getting a list of admins"""
    auth_client.admin()
    # All admins
    response = auth_client.get("/users?admin=true")
    assert response.status_code == status.HTTP_200_OK
    user_ids = [user["userId"] for user in response.json()['users']]
    user_ids.remove(auth_client.user.user_id)
    assert [data["user1"]] == user_ids


def test_get_users_from_edition(database_session: Session, auth_client: AuthClient, data: dict[str, str | int]):
    """Test endpoint for getting a list of users from a given edition"""
    auth_client.admin()
    # All users from edition
    response = auth_client.get(f"/users?edition={data['edition2']}")
    assert response.status_code == status.HTTP_200_OK
    user_ids = [user["userId"] for user in response.json()['users']]
    assert [data["user2"]] == user_ids


def test_get_admins_from_edition(database_session: Session, auth_client: AuthClient, data: dict[str, str | int]):
    """Test endpoint for getting a list of admins from a given edition"""
    auth_client.admin()
    # All admins from edition
    response = auth_client.get(f"/users?admin=true&edition={data['edition1']}")
    assert response.status_code == status.HTTP_200_OK
    user_ids = [user["userId"] for user in response.json()['users']]
    assert [data["user1"]] == user_ids

    response = auth_client.get(f"/users?admin=true&edition={data['edition2']}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['users']) == 0


def test_get_users_invalid(database_session: Session, auth_client: AuthClient, data: dict[str, str | int]):
    """Test endpoint for unvalid input"""
    auth_client.admin()
    # Invalid input
    response = auth_client.get("/users?admin=INVALID")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    response = auth_client.get("/users?edition=INVALID")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_edit_admin_status(database_session: Session, auth_client: AuthClient):
    """Test endpoint for editing the admin status of a user"""
    auth_client.admin()
    # Create user
    user = models.User(name="user1", email="user1@mail.com", admin=False)
    database_session.add(user)
    database_session.commit()

    response = auth_client.patch(f"/users/{user.user_id}",
                                 data=dumps({"admin": True}))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert user.admin

    response = auth_client.patch(f"/users/{user.user_id}",
                                 data=dumps({"admin": False}))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not user.admin


def test_add_coach(database_session: Session, auth_client: AuthClient):
    """Test endpoint for adding coaches"""
    auth_client.admin()
    # Create user
    user = models.User(name="user1", email="user1@mail.com", admin=False)
    database_session.add(user)

    # Create edition
    edition = models.Edition(year=1)
    database_session.add(edition)

    database_session.commit()

    # Add coach
    response = auth_client.post(f"/users/{user.user_id}/editions/{edition.edition_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    coach = database_session.query(user_editions).one()
    assert coach.user_id == user.user_id
    assert coach.edition_id == edition.edition_id


def test_remove_coach(database_session: Session, auth_client: AuthClient):
    """Test endpoint for removing coaches"""
    auth_client.admin()
    # Create user
    user = models.User(name="user1", email="user1@mail.com")
    database_session.add(user)

    # Create edition
    edition = models.Edition(year=1)
    database_session.add(edition)

    database_session.commit()

    # Create request
    request = models.CoachRequest(user_id=user.user_id, edition_id=edition.edition_id)
    database_session.add(request)

    database_session.commit()

    # Remove coach
    response = auth_client.delete(f"/users/{user.user_id}/editions/{edition.edition_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    coach = database_session.query(user_editions).all()
    assert len(coach) == 0


def test_get_all_requests(database_session: Session, auth_client: AuthClient):
    """Test endpoint for getting all userrequests"""
    auth_client.admin()

    # Create user
    user1 = models.User(name="user1", email="user1@mail.com")
    user2 = models.User(name="user2", email="user2@mail.com")
    database_session.add(user1)
    database_session.add(user2)

    # Create edition
    edition1 = models.Edition(year=1)
    edition2 = models.Edition(year=2)
    database_session.add(edition1)
    database_session.add(edition2)

    database_session.commit()

    # Create request
    request1 = models.CoachRequest(user_id=user1.user_id, edition_id=edition1.edition_id)
    request2 = models.CoachRequest(user_id=user2.user_id, edition_id=edition2.edition_id)
    database_session.add(request1)
    database_session.add(request2)

    database_session.commit()

    response = test_client.get(f"/users/requests")
    assert response.status_code == status.HTTP_200_OK
    user_ids = [request["user"]["userId"] for request in response.json()['requests']]
    assert len(user_ids) == 2
    assert user1.user_id in user_ids
    assert user2.user_id in user_ids


def test_get_all_requests_from_edition(database_session: Session, auth_client: AuthClient):
    """Test endpoint for getting all userrequests of a given edition"""
    auth_client.admin()

    # Create user
    user1 = models.User(name="user1", email="user1@mail.com")
    user2 = models.User(name="user2", email="user2@mail.com")
    database_session.add(user1)
    database_session.add(user2)

    # Create edition
    edition1 = models.Edition(year=1)
    edition2 = models.Edition(year=2)
    database_session.add(edition1)
    database_session.add(edition2)

    database_session.commit()

    # Create request
    request1 = models.CoachRequest(user_id=user1.user_id, edition_id=edition1.edition_id)
    request2 = models.CoachRequest(user_id=user2.user_id, edition_id=edition2.edition_id)
    database_session.add(request1)
    database_session.add(request2)

    database_session.commit()

    response = test_client.get(f"/users/requests?edition={edition1.edition_id}")
    assert response.status_code == status.HTTP_200_OK
    requests = response.json()['requests']
    assert len(requests) == 1
    assert user1.user_id == requests[0]["user"]["userId"]

    response = test_client.get(f"/users/requests?edition={edition2.edition_id}")
    assert response.status_code == status.HTTP_200_OK
    requests = response.json()['requests']
    assert len(requests) == 1
    assert user2.user_id == requests[0]["user"]["userId"]


def test_accept_request(database_session, auth_client: AuthClient):
    """Test endpoint for accepting a coach request"""
    auth_client.admin()
    # Create user
    user1 = models.User(name="user1", email="user1@mail.com")
    database_session.add(user1)

    # Create edition
    edition1 = models.Edition(year=1)
    database_session.add(edition1)

    database_session.commit()

    # Create request
    request1 = models.CoachRequest(user_id=user1.user_id, edition_id=edition1.edition_id)
    database_session.add(request1)

    database_session.commit()

    response = auth_client.post(f"users/requests/{request1.request_id}/accept")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert len(user1.editions) == 1
    assert user1.editions[0].edition_id == edition1.edition_id


def test_reject_request(database_session, auth_client: AuthClient):
    """Test endpoint for rejecting a coach request"""
    auth_client.admin()
    # Create user
    user1 = models.User(name="user1", email="user1@mail.com")
    database_session.add(user1)

    # Create edition
    edition1 = models.Edition(year=1)
    database_session.add(edition1)

    database_session.commit()

    # Create request
    request1 = models.CoachRequest(user_id=user1.user_id, edition_id=edition1.edition_id)
    database_session.add(request1)

    database_session.commit()

    response = auth_client.post(f"users/requests/{request1.request_id}/reject")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    requests = database_session.query(CoachRequest).all()
    assert len(requests) == 0

    response = auth_client.post("users/requests/INVALID/reject")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
