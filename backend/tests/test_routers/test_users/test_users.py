from sqlalchemy.orm import Session

from starlette.testclient import TestClient
from starlette import status

from json import dumps

from src.database import models
from src.database.models import user_editions


def test_get_users(db: Session, test_client: TestClient):
    # Create users
    user1 = models.User(name="user1", email="user1@mail.com", admin=True)
    db.add(user1)
    user2 = models.User(name="user2", email="user2@mail.com", admin=False)
    db.add(user2)

    # Create editions
    edition1 = models.Edition(year=1)
    db.add(edition1)
    edition2 = models.Edition(year=2)
    db.add(edition2)

    db.commit()

    # Create coach roles
    db.execute(models.user_editions.insert(), [
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


def test_edit_admin_status(db: Session, test_client: TestClient):
    # Create user
    user = models.User(name="user1", email="user1@mail.com", admin=False)
    db.add(user)
    db.commit()

    response = test_client.patch(f"/users/{user.user_id}",
                                 data=dumps({"admin": True}))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert user.admin

    response = test_client.patch(f"/users/{user.user_id}",
                                 data=dumps({"admin": False}))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not user.admin


def test_coach(db: Session, test_client: TestClient):
    # Create user
    user = models.User(name="user1", email="user1@mail.com", admin=False)
    db.add(user)

    # Create edition
    edition = models.Edition(year=1)
    db.add(edition)

    db.commit()

    # Add coach
    response = test_client.post(f"/users/{user.user_id}/editions/{edition.edition_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    coach = db.query(user_editions).one()
    assert coach.user_id == user.user_id
    assert coach.edition_id == edition.edition_id

    # Remove coach
    response = test_client.delete(f"/users/{user.user_id}/editions/{edition.edition_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    coach = db.query(user_editions).all()
    assert len(coach) == 0


# def test_accept_request(db, test_client: TestClient):
#     # Create user
#     user1 = models.User(name="user1", email="user1@mail.com")
#     db.add(user1)
#
#     db.commit()
#
#     # Create request
#     request1 = models.CoachRequest(user_id=user1.user_id)
#     db.add(request1)
#
#     # Create edition
#     edition1 = models.Edition(year=1)
#     db.add(edition1)
#
#     db.commit()
#
#     response = test_client.post(f"editions/{edition1.edition_id}/users/{user1.user_id}/request",
#                                 data=dumps({"accept": True}))
#     assert response.status_code == status.HTTP_204_NO_CONTENT
#
#     requests = db.query(CoachRequest).all()
#     assert len(requests) == 0
#
#     user_role: UserRole = db.query(UserRole).one()
#     assert user_role.role == RoleEnum.COACH
#     assert user_role.edition_id == edition1.edition_id
#     assert user_role.user_id == user1.user_id
#
#
# def test_reject_request_new_user(db, test_client: TestClient):
#
#     # Create user
#     user1 = models.User(name="user1", email="user1@mail.com")
#     db.add(user1)
#
#     db.commit()
#
#     # Create request
#     request1 = models.CoachRequest(user_id=user1.user_id)
#     db.add(request1)
#
#     # Create edition
#     edition1 = models.Edition(year=1)
#     db.add(edition1)
#
#     db.commit()
#
#     response = test_client.post(f"editions/{edition1.edition_id}/users/{user1.user_id}/request",
#                                 data=dumps({"accept": False}))
#     assert response.status_code == status.HTTP_204_NO_CONTENT
#
#     requests = db.query(CoachRequest).all()
#     assert len(requests) == 0
#
#     response = test_client.post(f"editions/{edition1.edition_id}/users/{user1.user_id}/request",
#                                 data=dumps({"accept": "INVALID INPUT"}))
#     assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
