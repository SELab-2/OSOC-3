from sqlalchemy.orm import Session

from src.database import models
import src.database.crud.users as users_crud
from src.database.models import user_editions, CoachRequest


def test_get_users(db: Session):
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


    # get all users
    users = users_crud.get_all_users(db)
    assert len(users) == 2, "Wrong length"
    user_ids = [user.user_id for user in users]
    assert user1.user_id in user_ids
    assert user2.user_id in user_ids

    # get all admins
    users = users_crud.get_all_admins(db)
    assert len(users) == 1, "Wrong length"
    assert user1.user_id == users[0].user_id

    # get all users from edition
    users = users_crud.get_users_from_edition(db, edition1.edition_id)
    assert len(users) == 2, "Wrong length"
    user_ids = [user.user_id for user in users]
    assert user1.user_id in user_ids
    assert user2.user_id in user_ids

    users = users_crud.get_users_from_edition(db, edition2.edition_id)
    assert len(users) == 1, "Wrong length"
    assert user2.user_id == users[0].user_id

    # get all admins from edition
    users = users_crud.get_admins_from_edition(db, edition1.edition_id)
    assert len(users) == 1, "Wrong length"
    assert user1.user_id == users[0].user_id

    users = users_crud.get_admins_from_edition(db, edition2.edition_id)
    assert len(users) == 0, "Wrong length"


def test_edit_admin_status(db: Session):
    # Create user
    user = models.User(name="user1", email="user1@mail.com", admin=False)
    db.add(user)
    db.commit()

    users_crud.edit_admin_status(db, user.user_id, True)
    assert user.admin

    users_crud.edit_admin_status(db, user.user_id, False)
    assert not user.admin


def test_coach(db: Session):
    # Create user
    user = models.User(name="user1", email="user1@mail.com", admin=False)
    db.add(user)

    # Create edition
    edition = models.Edition(year=1)
    db.add(edition)

    db.commit()

    users_crud.add_coach(db, user.user_id, edition.edition_id)
    coach = db.query(user_editions).one()
    assert coach.user_id == user.user_id
    assert coach.edition_id == edition.edition_id

    users_crud.remove_coach(db, user.user_id, edition.edition_id)
    assert len(db.query(user_editions).all()) == 0


def test_accept_request(db: Session):
    # Create user
    user1 = models.User(name="user1", email="user1@mail.com")
    db.add(user1)

    # Create edition
    edition1 = models.Edition(year=1)
    db.add(edition1)

    db.commit()

    # Create request
    request1 = models.CoachRequest(user_id=user1.user_id, edition_id=edition1.edition_id)
    db.add(request1)

    db.commit()

    users_crud.accept_request(db, request1.request_id)

    requests = db.query(CoachRequest).all()
    assert len(requests) == 0

    assert user1.editions[0].edition_id == edition1.edition_id



def test_reject_request_new_user(db: Session):

    # Create user
    user1 = models.User(name="user1", email="user1@mail.com")
    db.add(user1)

    # Create edition
    edition1 = models.Edition(year=1)
    db.add(edition1)

    db.commit()

    # Create request
    request1 = models.CoachRequest(user_id=user1.user_id, edition_id=edition1.edition_id)
    db.add(request1)

    db.commit()

    users_crud.reject_request(db, request1.request_id)

    requests = db.query(CoachRequest).all()
    assert len(requests) == 0
