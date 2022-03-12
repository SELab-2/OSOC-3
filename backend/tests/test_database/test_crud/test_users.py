from sqlalchemy.orm import Session

from src.database import models
import src.database.crud.users as users_crud
from src.database.enums import RoleEnum
from src.database.models import CoachRequest, User, UserRole


def test_get_users_from_edition(database_session: Session):
    # Create users
    user1 = models.User(name="user1", email="user1@mail.com")
    database_session.add(user1)
    user2 = models.User(name="user2", email="user2@mail.com")
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


def test_add_user_as_coach(database_session: Session):
    # Create user
    user1 = models.User(name="user1", email="user1@mail.com")
    database_session.add(user1)

    # Create edition
    edition1 = models.Edition(year=1)
    database_session.add(edition1)

    database_session.commit()

    # TODO


def test_accept_request(database_session: Session):
    # Create user
    user1 = models.User(name="user1", email="user1@mail.com")
    database_session.add(user1)

    database_session.commit()

    # Create request
    request1 = models.CoachRequest(user_id=user1.user_id)
    database_session.add(request1)

    # Create edition
    edition1 = models.Edition(year=1)
    database_session.add(edition1)

    database_session.commit()

    users_crud.accept_request(database_session, edition1.edition_id, user1.user_id)

    requests = database_session.query(CoachRequest).all()
    assert len(requests) == 0

    user_role: UserRole = database_session.query(UserRole).one()
    assert user_role.role == RoleEnum.COACH
    assert user_role.edition_id == edition1.edition_id
    assert user_role.user_id == user1.user_id


def test_reject_request_new_user(database_session: Session):

    # Create user
    user1 = models.User(name="user1", email="user1@mail.com")
    database_session.add(user1)

    database_session.commit()

    # Create request
    request1 = models.CoachRequest(user_id=user1.user_id)
    database_session.add(request1)

    database_session.commit()

    users_crud.reject_request(database_session, user1.user_id)

    requests = database_session.query(CoachRequest).all()
    assert len(requests) == 0


def test_reject_request_existing_user(database_session: Session):

    # Create user
    user1 = models.User(name="user1", email="user1@mail.com")
    database_session.add(user1)

    # Create editions
    edition1 = models.Edition(year=1)
    database_session.add(edition1)

    edition2 = models.Edition(year=2)
    database_session.add(edition2)

    database_session.commit()

    # Create request
    request1 = models.CoachRequest(user_id=user1.user_id)
    database_session.add(request1)

    # Create role
    user1_edition1_role = models.UserRole(user_id=user1.user_id, role=RoleEnum.COACH, edition_id=edition1.edition_id)
    database_session.add(user1_edition1_role)

    users_crud.reject_request(database_session, user1.user_id)

    requests = database_session.query(CoachRequest).all()
    assert len(requests) == 0

    user_roles: list[UserRole] = database_session.query(UserRole).all()
    assert len(user_roles) == 1
    assert user_roles[0].edition_id == edition1.edition_id
