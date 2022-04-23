import pytest
from sqlalchemy.orm import Session

import src.database.crud.users as users_crud
from settings import DB_PAGE_SIZE
from src.app.schemas.users import FilterParameters
from src.database import models
from src.database.models import user_editions, CoachRequest


@pytest.fixture
def data(database_session: Session) -> dict[str, str]:
    """Fill database with dummy data"""

    # Create users
    user1 = models.User(name="user1", admin=True)
    database_session.add(user1)
    user2 = models.User(name="user2", admin=False)
    database_session.add(user2)

    # Create editions
    edition1 = models.Edition(year=1, name="ed1")
    database_session.add(edition1)
    edition2 = models.Edition(year=2, name="ed2")
    database_session.add(edition2)

    database_session.commit()

    email_auth1 = models.AuthEmail(user_id=user1.user_id, email="user1@mail.com", pw_hash="HASH1")
    github_auth1 = models.AuthGitHub(user_id=user2.user_id, gh_auth_id=123, email="user2@mail.com")
    database_session.add(email_auth1)
    database_session.add(github_auth1)
    database_session.commit()

    # Create coach roles
    database_session.execute(models.user_editions.insert(), [
        {"user_id": user1.user_id, "edition_id": edition1.edition_id},
        {"user_id": user2.user_id, "edition_id": edition1.edition_id},
        {"user_id": user2.user_id, "edition_id": edition2.edition_id}
    ])

    return {"user1": user1.user_id,
            "user2": user2.user_id,
            "edition1": edition1.name,
            "edition2": edition2.name,
            "email1": "user1@mail.com"
            }


def test_get_all_users(database_session: Session, data: dict[str, int]):
    """Test get request for users"""

    # get all users
    users = users_crud.get_users_filtered_page(database_session, FilterParameters())
    assert len(users) == 2, "Wrong length"
    user_ids = [user.user_id for user in users]
    assert data["user1"] in user_ids
    assert data["user2"] in user_ids


def test_get_all_users_paginated(database_session: Session):
    for i in range(round(DB_PAGE_SIZE * 1.5)):
        database_session.add(models.User(name=f"User {i}", admin=False))
    database_session.commit()

    assert len(users_crud.get_users_filtered_page(database_session, FilterParameters(page=0))) == DB_PAGE_SIZE
    assert len(users_crud.get_users_filtered_page(database_session, FilterParameters(page=1))) == round(
        DB_PAGE_SIZE * 1.5
    ) - DB_PAGE_SIZE


def test_get_all_users_paginated_filter_name(database_session: Session):
    count = 0
    for i in range(round(DB_PAGE_SIZE * 1.5)):
        database_session.add(models.User(name=f"User {i}", admin=False))
        if "1" in str(i):
            count += 1
    database_session.commit()

    assert len(users_crud.get_users_filtered_page(database_session, FilterParameters(page=0, name="1"))) == count
    assert len(users_crud.get_users_filtered_page(database_session, FilterParameters(page=1, name="1"))) == max(
        count - round(
            DB_PAGE_SIZE * 1.5), 0)


def test_get_all_admins(database_session: Session, data: dict[str, str]):
    """Test get request for admins"""

    # get all admins
    users = users_crud.get_users_filtered_page(database_session, FilterParameters(admin=True))
    assert len(users) == 1, "Wrong length"
    assert data["user1"] == users[0].user_id


def test_get_all_admins_paginated(database_session: Session):
    admins = []
    for i in range(round(DB_PAGE_SIZE * 3)):
        user = models.User(name=f"User {i}", admin=i % 2 == 0)
        database_session.add(user)
        if i % 2 == 0:
            admins.append(user)
    database_session.commit()

    count = len(admins)
    users = users_crud.get_users_filtered_page(database_session, FilterParameters(page=0, admin=True))
    assert len(users) == min(count, DB_PAGE_SIZE)
    for user in users:
        assert user in admins

    assert len(users_crud.get_users_filtered_page(database_session, FilterParameters(page=1, admin=True))) == \
           min(count - DB_PAGE_SIZE, DB_PAGE_SIZE)


def test_get_all_non_admins_paginated(database_session: Session):
    non_admins = []
    for i in range(round(DB_PAGE_SIZE * 3)):
        user = models.User(name=f"User {i}", admin=i % 2 == 0)
        database_session.add(user)
        if i % 2 != 0:
            non_admins.append(user)
    database_session.commit()

    count = len(non_admins)
    users = users_crud.get_users_filtered_page(database_session, FilterParameters(page=0, admin=False))
    assert len(users) == min(count, DB_PAGE_SIZE)
    for user in users:
        assert user in non_admins

    assert len(users_crud.get_users_filtered_page(database_session, FilterParameters(page=1, admin=False))) == \
           min(count - DB_PAGE_SIZE, DB_PAGE_SIZE)


def test_get_all_admins_paginated_filter_name(database_session: Session):
    count = 0
    for i in range(round(DB_PAGE_SIZE * 1.5)):
        database_session.add(models.User(name=f"User {i}", admin=i % 2 == 0))
        if "1" in str(i) and i % 2 == 0:
            count += 1
    database_session.commit()

    assert len(
        users_crud.get_users_filtered_page(database_session, FilterParameters(page=0, name="1", admin=True))) == count
    assert len(
        users_crud.get_users_filtered_page(database_session, FilterParameters(page=1, name="1", admin=True))) == max(
        count - round(
            DB_PAGE_SIZE * 1.5), 0)


def test_get_user_edition_names_empty(database_session: Session):
    """Test getting all editions from a user when there are none"""
    user = models.User(name="test")
    database_session.add(user)
    database_session.commit()

    # No editions yet
    editions = users_crud.get_user_edition_names(database_session, user)
    assert len(editions) == 0


def test_get_user_edition_names_admin(database_session: Session):
    """Test getting all editions for an admin"""
    user = models.User(name="test", admin=True)
    database_session.add(user)

    edition = models.Edition(year=2022, name="ed2022")
    database_session.add(edition)
    database_session.commit()

    # Not added to edition yet, but admin can see it anyway
    editions = users_crud.get_user_edition_names(database_session, user)
    assert len(editions) == 1


def test_get_user_edition_names_coach(database_session: Session):
    """Test getting all editions for a coach when they aren't empty"""
    user = models.User(name="test")
    database_session.add(user)

    edition = models.Edition(year=2022, name="ed2022")
    database_session.add(edition)
    database_session.commit()

    # No editions yet
    editions = users_crud.get_user_edition_names(database_session, user)
    assert len(editions) == 0

    # Add user to a new edition
    user.editions.append(edition)
    database_session.add(user)
    database_session.commit()

    # No editions yet
    editions = users_crud.get_user_edition_names(database_session, user)
    assert editions == [edition.name]


def test_get_all_users_from_edition(database_session: Session, data: dict[str, str]):
    """Test get request for users of a given edition"""

    # get all users from edition
    users = users_crud.get_users_filtered_page(database_session, FilterParameters(edition=data["edition1"]))
    assert len(users) == 2, "Wrong length"
    user_ids = [user.user_id for user in users]
    assert data["user1"] in user_ids
    assert data["user2"] in user_ids

    users = users_crud.get_users_filtered_page(database_session, FilterParameters(edition=data["edition2"]))
    assert len(users) == 1, "Wrong length"
    assert data["user2"] == users[0].user_id


def test_get_all_users_for_edition_paginated(database_session: Session):
    edition_1 = models.Edition(year=2022, name="ed2022")
    edition_2 = models.Edition(year=2023, name="ed2023")
    database_session.add(edition_1)
    database_session.add(edition_2)
    database_session.commit()

    for i in range(round(DB_PAGE_SIZE * 1.5)):
        user_1 = models.User(name=f"User {i} - a", admin=False)
        user_2 = models.User(name=f"User {i} - b", admin=False)
        database_session.add(user_1)
        database_session.add(user_2)
        database_session.commit()
        database_session.execute(models.user_editions.insert(), [
            {"user_id": user_1.user_id, "edition_id": edition_1.edition_id},
            {"user_id": user_2.user_id, "edition_id": edition_2.edition_id},
        ])
    database_session.commit()

    assert len(users_crud.get_users_filtered_page(database_session, FilterParameters(edition=edition_1.name,
                                                                                     page=0))) == DB_PAGE_SIZE
    assert len(users_crud.get_users_filtered_page(database_session,
                                                  FilterParameters(edition=edition_1.name, page=1))) == round(
        DB_PAGE_SIZE * 1.5
    ) - DB_PAGE_SIZE
    assert len(users_crud.get_users_filtered_page(database_session, FilterParameters(edition=edition_2.name,
                                                                                     page=0))) == DB_PAGE_SIZE
    assert len(users_crud.get_users_filtered_page(database_session,
                                                  FilterParameters(edition=edition_2.name, page=1))) == round(
        DB_PAGE_SIZE * 1.5
    ) - DB_PAGE_SIZE


def test_get_all_users_for_edition_paginated_filter_name(database_session: Session):
    edition_1 = models.Edition(year=2022, name="ed2022")
    edition_2 = models.Edition(year=2023, name="ed2023")
    database_session.add(edition_1)
    database_session.add(edition_2)
    database_session.commit()

    count = 0
    for i in range(round(DB_PAGE_SIZE * 1.5)):
        user_1 = models.User(name=f"User {i} - a", admin=False)
        user_2 = models.User(name=f"User {i} - b", admin=False)
        database_session.add(user_1)
        database_session.add(user_2)
        database_session.commit()
        database_session.execute(models.user_editions.insert(), [
            {"user_id": user_1.user_id, "edition_id": edition_1.edition_id},
            {"user_id": user_2.user_id, "edition_id": edition_2.edition_id},
        ])
        if "1" in str(i):
            count += 1
    database_session.commit()

    assert len(users_crud.get_users_filtered_page(database_session,
                                                  FilterParameters(edition=edition_1.name, page=0, name="1"))) == \
           min(count, DB_PAGE_SIZE)
    assert len(users_crud.get_users_filtered_page(database_session,
                                                  FilterParameters(edition=edition_1.name, page=1, name="1"))) == \
           max(count - DB_PAGE_SIZE, 0)
    assert len(users_crud.get_users_filtered_page(database_session,
                                                  FilterParameters(edition=edition_2.name, page=0, name="1"))) == \
           min(count, DB_PAGE_SIZE)
    assert len(users_crud.get_users_filtered_page(database_session,
                                                  FilterParameters(edition=edition_2.name, page=1, name="1"))) == \
           max(count - DB_PAGE_SIZE, 0)


def test_get_all_users_excluded_edition_paginated(database_session: Session):
    edition_a = models.Edition(year=2022, name="edA")
    edition_b = models.Edition(year=2023, name="edB")
    database_session.add(edition_a)
    database_session.add(edition_b)
    database_session.commit()

    for i in range(round(DB_PAGE_SIZE * 1.5)):
        user_1 = models.User(name=f"User {i} - a", admin=False)
        user_2 = models.User(name=f"User {i} - b", admin=False)
        database_session.add(user_1)
        database_session.add(user_2)
        database_session.commit()
        database_session.execute(models.user_editions.insert(), [
            {"user_id": user_1.user_id, "edition_id": edition_a.edition_id},
            {"user_id": user_2.user_id, "edition_id": edition_b.edition_id},
        ])
    database_session.commit()

    a_users = users_crud.get_users_filtered_page(database_session,
                                                 FilterParameters(page=0, exclude_edition="edB", name=""))
    assert len(a_users) == DB_PAGE_SIZE
    for user in a_users:
        assert "b" not in user.name
    assert len(users_crud.get_users_filtered_page(database_session,
                                                  FilterParameters(page=1, exclude_edition="edB", name=""))) == \
           round(DB_PAGE_SIZE * 1.5) - DB_PAGE_SIZE

    b_users = users_crud.get_users_filtered_page(database_session,
                                                 FilterParameters(page=0, exclude_edition="edA", name=""))
    assert len(b_users) == DB_PAGE_SIZE
    for user in b_users:
        assert "a" not in user.name
    assert len(users_crud.get_users_filtered_page(database_session,
                                                  FilterParameters(page=1, exclude_edition="edA", name=""))) == \
           round(DB_PAGE_SIZE * 1.5) - DB_PAGE_SIZE


def test_get_all_users_excluded_edition_paginated_filter_name(database_session: Session):
    edition_a = models.Edition(year=2022, name="edA")
    edition_b = models.Edition(year=2023, name="edB")
    database_session.add(edition_a)
    database_session.add(edition_b)
    database_session.commit()

    count = 0
    for i in range(round(DB_PAGE_SIZE * 1.5)):
        user_1 = models.User(name=f"User {i} - a", admin=False)
        user_2 = models.User(name=f"User {i} - b", admin=False)
        database_session.add(user_1)
        database_session.add(user_2)
        database_session.commit()
        database_session.execute(models.user_editions.insert(), [
            {"user_id": user_1.user_id, "edition_id": edition_a.edition_id},
            {"user_id": user_2.user_id, "edition_id": edition_b.edition_id},
        ])
        if "1" in str(i):
            count += 1
    database_session.commit()

    a_users = users_crud.get_users_filtered_page(database_session,
                                                 FilterParameters(page=0, exclude_edition="edB", name="1"))
    assert len(a_users) == min(count, DB_PAGE_SIZE)
    for user in a_users:
        assert "b" not in user.name
    assert len(users_crud.get_users_filtered_page(database_session,
                                                  FilterParameters(page=1, exclude_edition="edB", name="1"))) == \
           max(count - DB_PAGE_SIZE, 0)

    b_users = users_crud.get_users_filtered_page(database_session,
                                                 FilterParameters(page=0, exclude_edition="edA", name="1"))
    assert len(b_users) == min(count, DB_PAGE_SIZE)
    for user in b_users:
        assert "a" not in user.name
    assert len(users_crud.get_users_filtered_page(database_session,
                                                  FilterParameters(page=1, exclude_edition="edA", name="1"))) == \
           max(count - DB_PAGE_SIZE, 0)


def test_get_all_users_for_edition_excluded_edition_paginated(database_session: Session):
    edition_a = models.Edition(year=2022, name="edA")
    edition_b = models.Edition(year=2023, name="edB")
    database_session.add(edition_a)
    database_session.add(edition_b)
    database_session.commit()

    correct_users = []
    for i in range(round(DB_PAGE_SIZE * 1.5)):
        user_1 = models.User(name=f"User {i} - a", admin=False)
        user_2 = models.User(name=f"User {i} - b", admin=False)
        database_session.add(user_1)
        database_session.add(user_2)
        database_session.commit()
        database_session.execute(models.user_editions.insert(), [
            {"user_id": user_1.user_id, "edition_id": edition_a.edition_id},
            {"user_id": user_2.user_id, "edition_id": edition_b.edition_id},
        ])
        if i % 2:
            database_session.execute(models.user_editions.insert(), [
                {"user_id": user_1.user_id, "edition_id": edition_b.edition_id},
            ])
        else:
            correct_users.append(user_1)

    database_session.commit()

    users = users_crud.get_users_filtered_page(database_session, FilterParameters(page=0, exclude_edition="edB",
                                                                                  edition="edA"))
    assert len(users) == len(correct_users)
    for user in users:
        assert user in correct_users


def test_edit_admin_status(database_session: Session):
    """Test changing the admin status of a user"""

    # Create user
    user = models.User(name="user1", admin=False)
    database_session.add(user)
    database_session.commit()

    users_crud.edit_admin_status(database_session, user.user_id, True)
    assert user.admin

    users_crud.edit_admin_status(database_session, user.user_id, False)
    assert not user.admin


def test_add_coach(database_session: Session):
    """Test adding a user as coach"""

    # Create user
    user = models.User(name="user1", admin=False)
    database_session.add(user)

    # Create edition
    edition = models.Edition(year=1, name="ed1")
    database_session.add(edition)

    database_session.commit()

    users_crud.add_coach(database_session, user.user_id, edition.name)
    coach = database_session.query(user_editions).one()
    assert coach.user_id == user.user_id
    assert coach.edition_id == edition.edition_id


def test_remove_coach(database_session: Session):
    """Test removing a user as coach"""

    # Create user
    user1 = models.User(name="user1", admin=False)
    database_session.add(user1)
    user2 = models.User(name="user2", admin=False)
    database_session.add(user2)

    # Create edition
    edition = models.Edition(year=1, name="ed1")
    database_session.add(edition)

    database_session.commit()

    # Create coach role
    database_session.execute(models.user_editions.insert(), [
        {"user_id": user1.user_id, "edition_id": edition.edition_id},
        {"user_id": user2.user_id, "edition_id": edition.edition_id}
    ])

    users_crud.remove_coach(database_session, user1.user_id, edition.name)
    assert len(database_session.query(user_editions).all()) == 1


def test_remove_coach_all_editions(database_session: Session):
    """Test removing a user as coach from all editions"""

    # Create user
    user1 = models.User(name="user1", admin=False)
    database_session.add(user1)
    user2 = models.User(name="user2", admin=False)
    database_session.add(user2)

    # Create edition
    edition1 = models.Edition(year=1, name="ed1")
    edition2 = models.Edition(year=2, name="ed2")
    edition3 = models.Edition(year=3, name="ed3")
    database_session.add(edition1)
    database_session.add(edition2)
    database_session.add(edition3)

    database_session.commit()

    # Create coach role
    database_session.execute(models.user_editions.insert(), [
        {"user_id": user1.user_id, "edition_id": edition1.edition_id},
        {"user_id": user1.user_id, "edition_id": edition2.edition_id},
        {"user_id": user1.user_id, "edition_id": edition3.edition_id},
        {"user_id": user2.user_id, "edition_id": edition2.edition_id},
    ])

    users_crud.remove_coach_all_editions(database_session, user1.user_id)
    assert len(database_session.query(user_editions).all()) == 1


def test_get_all_requests(database_session: Session):
    """Test get request for all userrequests"""
    # Create user
    user1 = models.User(name="user1")
    user2 = models.User(name="user2")
    database_session.add(user1)
    database_session.add(user2)

    # Create edition
    edition1 = models.Edition(year=1, name="ed1")
    edition2 = models.Edition(year=2, name="ed2")
    database_session.add(edition1)
    database_session.add(edition2)

    database_session.commit()

    # Create request
    request1 = models.CoachRequest(user_id=user1.user_id, edition_id=edition1.edition_id)
    request2 = models.CoachRequest(user_id=user2.user_id, edition_id=edition2.edition_id)
    database_session.add(request1)
    database_session.add(request2)

    database_session.commit()

    requests = users_crud.get_requests(database_session)
    assert len(requests) == 2
    assert request1 in requests
    assert request2 in requests
    users = [request.user for request in requests]
    assert user1 in users
    assert user2 in users


def test_get_requests_paginated(database_session: Session):
    edition = models.Edition(year=2022, name="ed2022")
    database_session.add(edition)

    for i in range(round(DB_PAGE_SIZE * 1.5)):
        user = models.User(name=f"User {i}", admin=False)
        database_session.add(user)
        database_session.add(CoachRequest(user=user, edition=edition))
    database_session.commit()

    assert len(users_crud.get_requests_page(database_session, 0)) == DB_PAGE_SIZE
    assert len(users_crud.get_requests_page(database_session, 1)) == round(
        DB_PAGE_SIZE * 1.5
    ) - DB_PAGE_SIZE


def test_get_requests_paginated_filter_user_name(database_session: Session):
    edition = models.Edition(year=2022, name="ed2022")
    database_session.add(edition)

    count = 0
    for i in range(round(DB_PAGE_SIZE * 1.5)):
        user = models.User(name=f"User {i}", admin=False)
        database_session.add(user)
        database_session.add(CoachRequest(user=user, edition=edition))
        if "1" in str(i):
            count += 1
    database_session.commit()

    assert len(users_crud.get_requests_page(database_session, 0, "1")) == \
           min(DB_PAGE_SIZE, count)
    assert len(users_crud.get_requests_page(database_session, 1, "1")) == \
           max(count - DB_PAGE_SIZE, 0)


def test_get_all_requests_from_edition(database_session: Session):
    """Test get request for all userrequests of a given edition"""

    # Create user
    user1 = models.User(name="user1")
    user2 = models.User(name="user2")
    database_session.add(user1)
    database_session.add(user2)

    # Create edition
    edition1 = models.Edition(year=1, name="ed1")
    edition2 = models.Edition(year=2, name="ed2")
    database_session.add(edition1)
    database_session.add(edition2)

    database_session.commit()

    # Create request
    request1 = models.CoachRequest(user_id=user1.user_id, edition_id=edition1.edition_id)
    request2 = models.CoachRequest(user_id=user2.user_id, edition_id=edition2.edition_id)
    database_session.add(request1)
    database_session.add(request2)

    database_session.commit()

    requests = users_crud.get_requests_for_edition(database_session, edition1.name)
    assert len(requests) == 1
    assert requests[0].user == user1

    requests = users_crud.get_requests_for_edition(database_session, edition2.name)
    assert len(requests) == 1
    assert requests[0].user == user2


def test_get_requests_for_edition_paginated(database_session: Session):
    edition = models.Edition(year=2022, name="ed2022")
    database_session.add(edition)

    for i in range(round(DB_PAGE_SIZE * 1.5)):
        user = models.User(name=f"User {i}", admin=False)
        database_session.add(user)
        database_session.add(CoachRequest(user=user, edition=edition))
    database_session.commit()

    assert len(users_crud.get_requests_for_edition_page(database_session, edition.name, 0)) == DB_PAGE_SIZE
    assert len(users_crud.get_requests_for_edition_page(database_session, edition.name, 1)) == round(
        DB_PAGE_SIZE * 1.5
    ) - DB_PAGE_SIZE


def test_get_requests_for_edition_paginated_filter_user_name(database_session: Session):
    edition = models.Edition(year=2022, name="ed2022")
    database_session.add(edition)

    count = 0
    for i in range(round(DB_PAGE_SIZE * 1.5)):
        user = models.User(name=f"User {i}", admin=False)
        database_session.add(user)
        database_session.add(CoachRequest(user=user, edition=edition))
        if "1" in str(i):
            count += 1
    database_session.commit()

    assert len(users_crud.get_requests_for_edition_page(database_session, edition.name, 0, "1")) == \
           min(DB_PAGE_SIZE, count)
    assert len(users_crud.get_requests_for_edition_page(database_session, edition.name, 1, "1")) == \
           max(count - DB_PAGE_SIZE, 0)


def test_accept_request(database_session: Session):
    """Test accepting a coach request"""

    # Create user
    user1 = models.User(name="user1")
    database_session.add(user1)

    # Create edition
    edition1 = models.Edition(year=1, name="ed1")
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
    user1 = models.User(name="user1")
    database_session.add(user1)

    # Create edition
    edition1 = models.Edition(year=1, name="ed2022")
    database_session.add(edition1)
    database_session.commit()

    # Create request
    request1 = models.CoachRequest(user_id=user1.user_id, edition_id=edition1.edition_id)
    database_session.add(request1)
    database_session.commit()

    users_crud.reject_request(database_session, request1.request_id)

    requests = database_session.query(CoachRequest).all()
    assert len(requests) == 0


def test_remove_request_if_exists_exists(database_session: Session):
    """Test deleting a request when it exists"""
    user = models.User(name="user1")
    database_session.add(user)

    edition = models.Edition(year=2022, name="ed2022")
    database_session.add(edition)
    database_session.commit()

    request = models.CoachRequest(user_id=user.user_id, edition_id=edition.edition_id)
    database_session.add(request)
    database_session.commit()

    assert database_session.query(CoachRequest).count() == 1

    # Remove the request
    users_crud.remove_request_if_exists(database_session, user.user_id, edition.name)

    assert database_session.query(CoachRequest).count() == 0


def test_remove_request_if_not_exists(database_session: Session):
    """Test deleting a request when it doesn't exist"""
    user = models.User(name="user1")
    database_session.add(user)

    edition = models.Edition(year=2022, name="ed2022")
    database_session.add(edition)
    database_session.commit()

    # Remove the request
    # If the test succeeds then it means no error was raised, even though the request
    # doesn't exist
    users_crud.remove_request_if_exists(database_session, user.user_id, edition.name)
