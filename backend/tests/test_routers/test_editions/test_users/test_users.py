from sqlalchemy.orm import Session

from starlette.testclient import TestClient
from starlette import status

from src.database import models
from src.database.enums import RoleEnum


def test_get_users(database_session: Session, test_client: TestClient):
    # Create users
    user1 = models.User(name="user1", email="email1")
    database_session.add(user1)

    # Create editions
    edition1 = models.Edition(year=1)
    database_session.add(edition1)

    database_session.commit()

    # Create roles
    user1_edition1_role = models.UserRole(user_id=user1.user_id, role=RoleEnum.COACH, edition_id=edition1.edition_id)
    database_session.add(user1_edition1_role)

    database_session.commit()

    response = test_client.get(f"/editions/{edition1.edition_id}/users")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()


