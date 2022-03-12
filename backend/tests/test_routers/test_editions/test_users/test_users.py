from sqlalchemy.orm import Session

from starlette.testclient import TestClient
from starlette import status

from json import dumps

from src.app.schemas.users import Status
from src.database import models
from src.database.enums import RoleEnum


def test_get_users(database_session: Session, test_client: TestClient):
    # Create user
    user1 = models.User(name="user1", email="user1@mail.com")
    database_session.add(user1)

    # Create edition
    edition1 = models.Edition(year=1)
    database_session.add(edition1)

    database_session.commit()

    # Create role
    user1_edition1_role = models.UserRole(user_id=user1.user_id, role=RoleEnum.COACH, edition_id=edition1.edition_id)
    database_session.add(user1_edition1_role)

    database_session.commit()

    response = test_client.get(f"/editions/{edition1.edition_id}/users")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['users'][0]['userId'] == user1.user_id


def test_update_user_status(database_session: Session, test_client: TestClient):
    # Create user
    user1 = models.User(name="user1", email="user1@mail.com")
    database_session.add(user1)

    # Create edition
    edition1 = models.Edition(year=1)
    database_session.add(edition1)

    database_session.commit()

    # Create role
    user1_edition1_role = models.UserRole(user_id=user1.user_id, role=RoleEnum.COACH, edition_id=edition1.edition_id)
    database_session.add(user1_edition1_role)

    database_session.commit()

    response = test_client.patch(f"/editions/{edition1.edition_id}/users/{user1.user_id}/status", data=dumps({"status": Status.DISABLED.value}))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert user1_edition1_role.role == RoleEnum.DISABLED

    response = test_client.patch(f"/editions/{edition1.edition_id}/users/{user1.user_id}/status", data=dumps({"status": "INVALID STATUS"}))
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    response = test_client.patch(f"/editions/{edition1.edition_id}/users/{user1.user_id+1}", data=dumps({"status": Status.DISABLED.value}))
    assert response.status_code == status.HTTP_404_NOT_FOUND
