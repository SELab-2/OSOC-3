from sqlalchemy.orm import Session

from src.database import models
import src.database.crud.users as users_crud
from src.database.enums import RoleEnum


def test_get_users_from_edition(database_session: Session):
    # Create users
    user1 = models.User(name="user1", email="email1")
    database_session.add(user1)
    user2 = models.User(name="user2", email="email2")
    database_session.add(user2)

    # Create editions
    edition1 = models.Edition(year=1)
    database_session.add(edition1)
    edition2 = models.Edition(year=2)
    database_session.add(edition2)

    database_session.commit()

    # Create roles
    user1_edition1_role = models.UserRole(user_id=user1.user_id, role=RoleEnum.COACH, edition_id=edition1.edition_id)
    database_session.add(user1_edition1_role)
    user2_edition1_role = models.UserRole(user_id=user2.user_id, role=RoleEnum.COACH, edition_id=edition1.edition_id)
    database_session.add(user2_edition1_role)
    user2_edition2_role = models.UserRole(user_id=user2.user_id, role=RoleEnum.COACH, edition_id=edition2.edition_id)
    database_session.add(user2_edition2_role)

    database_session.commit()

    users = users_crud.get_users_from_edition(database_session, edition1.edition_id)
    assert len(users) == 2, "Wrong length"
    user_ids = [user.user_id for user in users]
    assert user1.user_id in user_ids
    assert user2.user_id in user_ids

    users = users_crud.get_users_from_edition(database_session, edition2.edition_id)
    assert len(users) == 1, "Wrong length"
    assert user2.user_id == users[0].user_id


def test_update_user_status(database_session: Session):
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

    users_crud.update_user_status(database_session, edition1.edition_id, user1.user_id, RoleEnum.DISABLED)
    assert user1_edition1_role.role == RoleEnum.DISABLED
