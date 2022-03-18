import pytest
from sqlalchemy.orm import Session

from src.database import models
import src.database.crud.users as users_crud
from src.database.models import user_editions, CoachRequest


@pytest.fixture
def data(database_session: Session) -> {str: str}:
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


def test_get_all_users(database_session: Session, data: {str: str}):
    """Test get request for users"""

    # get all users
    users = users_crud.get_all_users(database_session)
    assert len(users) == 2, "Wrong length"
    user_ids = [user.user_id for user in users]
    assert data["user1"] in user_ids
    assert data["user2"] in user_ids


def test_get_all_admins(database_session: Session, data: {str: str}):
    """Test get request for admins"""

    # get all admins
    users = users_crud.get_all_admins(database_session)
    assert len(users) == 1, "Wrong length"
    assert data["user1"] == users[0].user_id


def test_get_all_users_from_edition(database_session: Session, data: {str: str}):
    """Test get request for users of a given edition"""

    # get all users from edition
    users = users_crud.get_users_from_edition(database_session, data["edition1"])
    assert len(users) == 2, "Wrong length"
    user_ids = [user.user_id for user in users]
    assert data["user1"] in user_ids
    assert data["user2"] in user_ids

    users = users_crud.get_users_from_edition(database_session, data["edition2"])
    assert len(users) == 1, "Wrong length"
    assert data["user2"] == users[0].user_id


def test_get_admins_from_edition(database_session: Session, data: {str: str}):
    """Test get request for admins of a given edition"""

    # get all admins from edition
    users = users_crud.get_admins_from_edition(database_session, data["edition1"])
    assert len(users) == 1, "Wrong length"
    assert data["user1"] == users[0].user_id

    users = users_crud.get_admins_from_edition(database_session, data["edition2"])
    assert len(users) == 0, "Wrong length"


def test_edit_admin_status(database_session: Session):
    """Test changing the admin status of a user"""

    # Create user
    user = models.User(name="user1", email="user1@mail.com", admin=False)
    database_session.add(user)
    database_session.commit()

    users_crud.edit_admin_status(database_session, user.user_id, True)
    assert user.admin

    users_crud.edit_admin_status(database_session, user.user_id, False)
    assert not user.admin


def test_coach(database_session: Session):
    """Test adding a user as admin"""

    # Create user
    user = models.User(name="user1", email="user1@mail.com", admin=False)
    database_session.add(user)

    # Create edition
    edition = models.Edition(year=1)
    database_session.add(edition)

    database_session.commit()

    users_crud.add_coach(database_session, user.user_id, edition.edition_id)
    coach = database_session.query(user_editions).one()
    assert coach.user_id == user.user_id
    assert coach.edition_id == edition.edition_id

    users_crud.remove_coach(database_session, user.user_id, edition.edition_id)
    assert len(database_session.query(user_editions).all()) == 0


def test_accept_request(database_session: Session):
    """Test accepting a coach request"""

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

    users_crud.accept_request(database_session, request1.request_id)

    requests = database_session.query(CoachRequest).all()
    assert len(requests) == 0

    assert user1.editions[0].edition_id == edition1.edition_id


def test_reject_request_new_user(database_session: Session):
    """Test rejecting a coach request"""

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

    users_crud.reject_request(database_session, request1.request_id)

    requests = database_session.query(CoachRequest).all()
    assert len(requests) == 0
