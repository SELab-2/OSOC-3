from sqlalchemy.orm import Session

from starlette.testclient import TestClient
from starlette import status

from json import dumps

from src.database import models
from src.database.models import user_editions, CoachRequest


def test_get_users(database_session: Session, test_client: TestClient):
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

    # All users
    response = test_client.get(f"/users")
    assert response.status_code == status.HTTP_200_OK
    user_ids = [user["userId"] for user in response.json()['users']]
    assert len(user_ids) == 2
    assert user1.user_id in user_ids
    assert user2.user_id in user_ids

    # All admins
    response = test_client.get(f"/users?admin=true")
    assert response.status_code == status.HTTP_200_OK
    user_ids = [user["userId"] for user in response.json()['users']]
    assert [user1.user_id] == user_ids

    # All users from edition
    response = test_client.get(f"/users?edition={edition2.edition_id}")
    assert response.status_code == status.HTTP_200_OK
    user_ids = [user["userId"] for user in response.json()['users']]
    assert [user2.user_id] == user_ids

    # All admins from edition
    response = test_client.get(f"/users?admin=true&edition={edition1.edition_id}")
    assert response.status_code == status.HTTP_200_OK
    user_ids = [user["userId"] for user in response.json()['users']]
    assert [user1.user_id] == user_ids

    response = test_client.get(f"/users?admin=true&edition={edition2.edition_id}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['users']) == 0

    # Invalid input
    response = test_client.get(f"/users?admin=INVALID")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    response = test_client.get(f"/users?edition=INVALID")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_edit_admin_status(database_session: Session, test_client: TestClient):
    # Create user
    user = models.User(name="user1", email="user1@mail.com", admin=False)
    database_session.add(user)
    database_session.commit()

    response = test_client.patch(f"/users/{user.user_id}",
                                 data=dumps({"admin": True}))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert user.admin

    response = test_client.patch(f"/users/{user.user_id}",
                                 data=dumps({"admin": False}))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not user.admin


def test_coach(database_session: Session, test_client: TestClient):
    # Create user
    user = models.User(name="user1", email="user1@mail.com", admin=False)
    database_session.add(user)

    # Create edition
    edition = models.Edition(year=1)
    database_session.add(edition)

    database_session.commit()

    # Add coach
    response = test_client.post(f"/users/{user.user_id}/editions/{edition.edition_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    coach = database_session.query(user_editions).one()
    assert coach.user_id == user.user_id
    assert coach.edition_id == edition.edition_id

    # Remove coach
    response = test_client.delete(f"/users/{user.user_id}/editions/{edition.edition_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    coach = database_session.query(user_editions).all()
    assert len(coach) == 0


def test_accept_request(database_session, test_client: TestClient):
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

    response = test_client.post(f"users/requests/{request1.request_id}/accept")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert len(user1.editions) == 1
    assert user1.editions[0].edition_id == edition1.edition_id


def test_reject_request(database_session, test_client: TestClient):
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

    response = test_client.post(f"users/requests/{request1.request_id}/reject")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    requests = database_session.query(CoachRequest).all()
    assert len(requests) == 0

    response = test_client.post(f"users/requests/INVALID/reject")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
