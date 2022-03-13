from sqlalchemy.orm import Session

from starlette.testclient import TestClient
from starlette import status

from json import dumps

from src.app.schemas.users import Status
from src.database import models
from src.database.enums import RoleEnum
from src.database.models import CoachRequest, UserRole


def test_get_users(db, test_client: TestClient):
    # Create user
    user1 = models.User(name="user1", email="user1@mail.com")
    db.add(user1)

    # Create edition
    edition1 = models.Edition(year=1)
    db.add(edition1)

    db.commit()

    # Create role
    user1_edition1_role = models.UserRole(user_id=user1.user_id, role=RoleEnum.COACH, edition_id=edition1.edition_id)
    db.add(user1_edition1_role)

    db.commit()

    response = test_client.get(f"/editions/{edition1.edition_id}/users")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['users'][0]['userId'] == user1.user_id


def test_update_user_status(db, test_client: TestClient):
    # Create user
    user1 = models.User(name="user1", email="user1@mail.com")
    db.add(user1)

    # Create edition
    edition1 = models.Edition(year=1)
    db.add(edition1)

    db.commit()

    # Create role
    user1_edition1_role = models.UserRole(user_id=user1.user_id, role=RoleEnum.COACH, edition_id=edition1.edition_id)
    db.add(user1_edition1_role)

    db.commit()

    response = test_client.patch(f"/editions/{edition1.edition_id}/users/{user1.user_id}/status",
                                 data=dumps({"status": Status.DISABLED.value}))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert user1_edition1_role.role == RoleEnum.DISABLED

    response = test_client.patch(f"/editions/{edition1.edition_id}/users/{user1.user_id}/status",
                                 data=dumps({"status": "INVALID STATUS"}))
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    response = test_client.patch(f"/editions/{edition1.edition_id}/users/{user1.user_id+1}",
                                 data=dumps({"status": Status.DISABLED.value}))
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_accept_request(db, test_client: TestClient):
    # Create user
    user1 = models.User(name="user1", email="user1@mail.com")
    db.add(user1)

    db.commit()

    # Create request
    request1 = models.CoachRequest(user_id=user1.user_id)
    db.add(request1)

    # Create edition
    edition1 = models.Edition(year=1)
    db.add(edition1)

    db.commit()

    response = test_client.post(f"editions/{edition1.edition_id}/users/{user1.user_id}/request",
                                data=dumps({"accept": True}))
    assert response.status_code == status.HTTP_204_NO_CONTENT

    requests = db.query(CoachRequest).all()
    assert len(requests) == 0

    user_role: UserRole = db.query(UserRole).one()
    assert user_role.role == RoleEnum.COACH
    assert user_role.edition_id == edition1.edition_id
    assert user_role.user_id == user1.user_id


def test_reject_request_new_user(db, test_client: TestClient):

    # Create user
    user1 = models.User(name="user1", email="user1@mail.com")
    db.add(user1)

    db.commit()

    # Create request
    request1 = models.CoachRequest(user_id=user1.user_id)
    db.add(request1)

    # Create edition
    edition1 = models.Edition(year=1)
    db.add(edition1)

    db.commit()

    response = test_client.post(f"editions/{edition1.edition_id}/users/{user1.user_id}/request",
                                data=dumps({"accept": False}))
    assert response.status_code == status.HTTP_204_NO_CONTENT

    requests = db.query(CoachRequest).all()
    assert len(requests) == 0

    response = test_client.post(f"editions/{edition1.edition_id}/users/{user1.user_id}/request",
                                data=dumps({"accept": "INVALID INPUT"}))
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
