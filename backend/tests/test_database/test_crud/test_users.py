import pytest
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

import src.database.crud.users as users_crud
from settings import DB_PAGE_SIZE
from src.app.schemas.users import FilterParameters
from src.database import models
from src.database.models import user_editions, CoachRequest


@pytest.fixture
async def data(database_session: AsyncSession) -> dict[str, str]:
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

    await database_session.commit()

    email_auth1 = models.AuthEmail(user_id=user1.user_id, email="user1@mail.com", pw_hash="HASH1")
    github_auth1 = models.AuthGitHub(user_id=user2.user_id, gh_auth_id=123, email="user2@mail.com", github_user_id=2)
    database_session.add(email_auth1)
    database_session.add(github_auth1)
    await database_session.commit()

    # Create coach roles
    await database_session.execute(models.user_editions.insert(), [
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


async def test_get_all_users(database_session: AsyncSession, data: dict[str, int]):
    """Test get request for users"""

    # get all users
    users = await users_crud.get_users_filtered_page(database_session, FilterParameters())
    assert len(users) == 2, "Wrong length"
    user_ids = [user.user_id for user in users]
    assert data["user1"] in user_ids
    assert data["user2"] in user_ids


async def test_get_all_users_paginated(database_session: AsyncSession):
    for i in range(round(DB_PAGE_SIZE * 1.5)):
        database_session.add(models.User(name=f"User {i}", admin=False))
    await database_session.commit()

    assert len(await users_crud.get_users_filtered_page(database_session, FilterParameters(page=0))) == DB_PAGE_SIZE
    assert len(await users_crud.get_users_filtered_page(database_session, FilterParameters(page=1))) == round(
        DB_PAGE_SIZE * 1.5
    ) - DB_PAGE_SIZE


async def test_get_all_users_paginated_filter_name(database_session: AsyncSession):
    count = 0
    for i in range(round(DB_PAGE_SIZE * 1.5)):
        database_session.add(models.User(name=f"User {i}", admin=False))
        if "1" in str(i):
            count += 1
    await database_session.commit()

    assert len(await users_crud.get_users_filtered_page(database_session, FilterParameters(page=0, name="1"))) == count
    assert len(await users_crud.get_users_filtered_page(database_session, FilterParameters(page=1, name="1"))) == max(
        count - round(
            DB_PAGE_SIZE * 1.5), 0)


async def test_get_all_admins(database_session: AsyncSession, data: dict[str, str]):
    """Test get request for admins"""

    # get all admins
    users = await users_crud.get_users_filtered_page(database_session, FilterParameters(admin=True))
    assert len(users) == 1, "Wrong length"
    assert data["user1"] == users[0].user_id


async def test_get_all_admins_paginated(database_session: AsyncSession):
    admins = []
    for i in range(round(DB_PAGE_SIZE * 3)):
        user = models.User(name=f"User {i}", admin=i % 2 == 0)
        database_session.add(user)
        if i % 2 == 0:
            admins.append(user)
    await database_session.commit()

    count = len(admins)
    users = await users_crud.get_users_filtered_page(database_session, FilterParameters(page=0, admin=True))
    assert len(users) == min(count, DB_PAGE_SIZE)
    for user in users:
        assert user in admins

    assert len(await users_crud.get_users_filtered_page(database_session, FilterParameters(page=1, admin=True))) == \
           min(count - DB_PAGE_SIZE, DB_PAGE_SIZE)


async def test_get_all_non_admins_paginated(database_session: AsyncSession):
    non_admins = []
    for i in range(round(DB_PAGE_SIZE * 3)):
        user = models.User(name=f"User {i}", admin=i % 2 == 0)
        database_session.add(user)
        if i % 2 != 0:
            non_admins.append(user)
    await database_session.commit()

    count = len(non_admins)
    users = await users_crud.get_users_filtered_page(database_session, FilterParameters(page=0, admin=False))
    assert len(users) == min(count, DB_PAGE_SIZE)
    for user in users:
        assert user in non_admins

    assert len(await users_crud.get_users_filtered_page(database_session, FilterParameters(page=1, admin=False))) == \
           min(count - DB_PAGE_SIZE, DB_PAGE_SIZE)


async def test_get_all_admins_paginated_filter_name(database_session: AsyncSession):
    count = 0
    for i in range(round(DB_PAGE_SIZE * 1.5)):
        database_session.add(models.User(name=f"User {i}", admin=i % 2 == 0))
        if "1" in str(i) and i % 2 == 0:
            count += 1
    await database_session.commit()

    assert len(
        await users_crud.get_users_filtered_page(database_session,
                                                 FilterParameters(page=0, name="1", admin=True))) == count
    assert len(
        await users_crud.get_users_filtered_page(database_session,
                                                 FilterParameters(page=1, name="1", admin=True))) == max(
        count - round(
            DB_PAGE_SIZE * 1.5), 0)


async def test_get_user_editions_empty(database_session: AsyncSession):
    """Test getting all editions from a user when there are none"""
    user = models.User(name="test")
    database_session.add(user)
    await database_session.commit()

    # query the user to initiate association tables
    await database_session.execute(select(models.User).where(models.User.user_id == user.user_id))
    # No editions yet
    editions = await users_crud.get_user_editions(database_session, user)
    assert len(editions) == 0


async def test_get_user_editions_admin(database_session: AsyncSession):
    """Test getting all editions for an admin"""
    user = models.User(name="test", admin=True)
    database_session.add(user)

    edition = models.Edition(year=2022, name="ed2022")
    database_session.add(edition)
    await database_session.commit()

    # query the user to initiate association tables
    await database_session.execute(select(models.User).where(models.User.user_id == user.user_id))

    # Not added to edition yet, but admin can see it anyway
    editions = await users_crud.get_user_editions(database_session, user)
    assert len(editions) == 1


async def test_get_user_editions_coach(database_session: AsyncSession):
    """Test getting all editions for a coach when they aren't empty"""
    user = models.User(name="test")
    database_session.add(user)

    edition = models.Edition(year=2022, name="ed2022")
    database_session.add(edition)
    await database_session.commit()

    # query the user to initiate association tables
    await database_session.execute(select(models.User).where(models.User.user_id == user.user_id))

    # No editions yet
    editions = await users_crud.get_user_editions(database_session, user)
    assert len(editions) == 0

    # Add user to a new edition
    user.editions.append(edition)
    database_session.add(user)
    await database_session.commit()

    editions = await users_crud.get_user_editions(database_session, user)
    assert editions[0].name == edition.name


async def test_get_all_users_from_edition(database_session: AsyncSession, data: dict[str, str]):
    """Test get request for users of a given edition"""

    # get all users from edition
    users = await users_crud.get_users_filtered_page(database_session, FilterParameters(edition=data["edition1"]))
    assert len(users) == 2, "Wrong length"
    user_ids = [user.user_id for user in users]
    assert data["user1"] in user_ids
    assert data["user2"] in user_ids

    users = await users_crud.get_users_filtered_page(database_session, FilterParameters(edition=data["edition2"]))
    assert len(users) == 1, "Wrong length"
    assert data["user2"] == users[0].user_id


async def test_get_all_users_for_edition_paginated(database_session: AsyncSession):
    edition_1 = models.Edition(year=2022, name="ed2022")
    edition_2 = models.Edition(year=2023, name="ed2023")
    database_session.add(edition_1)
    database_session.add(edition_2)
    await database_session.commit()

    for i in range(round(DB_PAGE_SIZE * 1.5)):
        user_1 = models.User(name=f"User {i} - a", admin=False)
        user_2 = models.User(name=f"User {i} - b", admin=False)
        database_session.add(user_1)
        database_session.add(user_2)
        await database_session.commit()
        await database_session.execute(models.user_editions.insert(), [
            {"user_id": user_1.user_id, "edition_id": edition_1.edition_id},
            {"user_id": user_2.user_id, "edition_id": edition_2.edition_id},
        ])
    await database_session.commit()

    assert len(await users_crud.get_users_filtered_page(database_session, FilterParameters(edition=edition_1.name,
                                                                                           page=0))) == DB_PAGE_SIZE
    assert len(await users_crud.get_users_filtered_page(database_session,
                                                        FilterParameters(edition=edition_1.name, page=1))) == round(
        DB_PAGE_SIZE * 1.5
    ) - DB_PAGE_SIZE
    assert len(await users_crud.get_users_filtered_page(database_session, FilterParameters(edition=edition_2.name,
                                                                                           page=0))) == DB_PAGE_SIZE
    assert len(await users_crud.get_users_filtered_page(database_session,
                                                        FilterParameters(edition=edition_2.name, page=1))) == round(
        DB_PAGE_SIZE * 1.5
    ) - DB_PAGE_SIZE


async def test_get_all_users_for_edition_paginated_filter_name(database_session: AsyncSession):
    edition_1 = models.Edition(year=2022, name="ed2022")
    edition_2 = models.Edition(year=2023, name="ed2023")
    database_session.add(edition_1)
    database_session.add(edition_2)
    await database_session.commit()

    count = 0
    for i in range(round(DB_PAGE_SIZE * 1.5)):
        user_1 = models.User(name=f"User {i} - a", admin=False)
        user_2 = models.User(name=f"User {i} - b", admin=False)
        database_session.add(user_1)
        database_session.add(user_2)
        await database_session.commit()
        await database_session.execute(models.user_editions.insert(), [
            {"user_id": user_1.user_id, "edition_id": edition_1.edition_id},
            {"user_id": user_2.user_id, "edition_id": edition_2.edition_id},
        ])
        if "1" in str(i):
            count += 1
    await database_session.commit()

    assert len(await users_crud.get_users_filtered_page(database_session,
                                                        FilterParameters(edition=edition_1.name, page=0, name="1"))) == \
           min(count, DB_PAGE_SIZE)
    assert len(await users_crud.get_users_filtered_page(database_session,
                                                        FilterParameters(edition=edition_1.name, page=1, name="1"))) == \
           max(count - DB_PAGE_SIZE, 0)
    assert len(await users_crud.get_users_filtered_page(database_session,
                                                        FilterParameters(edition=edition_2.name, page=0, name="1"))) == \
           min(count, DB_PAGE_SIZE)
    assert len(await users_crud.get_users_filtered_page(database_session,
                                                        FilterParameters(edition=edition_2.name, page=1, name="1"))) == \
           max(count - DB_PAGE_SIZE, 0)


async def test_get_all_users_excluded_edition_paginated(database_session: AsyncSession):
    edition_a = models.Edition(year=2022, name="edA")
    edition_b = models.Edition(year=2023, name="edB")
    database_session.add(edition_a)
    database_session.add(edition_b)
    await database_session.commit()

    for i in range(round(DB_PAGE_SIZE * 1.5)):
        user_1 = models.User(name=f"User {i} - a", admin=False)
        user_2 = models.User(name=f"User {i} - b", admin=False)
        database_session.add(user_1)
        database_session.add(user_2)
        await database_session.commit()
        await database_session.execute(models.user_editions.insert(), [
            {"user_id": user_1.user_id, "edition_id": edition_a.edition_id},
            {"user_id": user_2.user_id, "edition_id": edition_b.edition_id},
        ])
    await database_session.commit()

    a_users = await users_crud.get_users_filtered_page(database_session,
                                                       FilterParameters(page=0, exclude_edition="edB", name=""))
    assert len(a_users) == DB_PAGE_SIZE
    for user in a_users:
        assert "b" not in user.name
    assert len(await users_crud.get_users_filtered_page(database_session,
                                                        FilterParameters(page=1, exclude_edition="edB", name=""))) == \
           round(DB_PAGE_SIZE * 1.5) - DB_PAGE_SIZE

    b_users = await users_crud.get_users_filtered_page(database_session,
                                                       FilterParameters(page=0, exclude_edition="edA", name=""))
    assert len(b_users) == DB_PAGE_SIZE
    for user in b_users:
        assert "a" not in user.name
    assert len(await users_crud.get_users_filtered_page(database_session,
                                                        FilterParameters(page=1, exclude_edition="edA", name=""))) == \
           round(DB_PAGE_SIZE * 1.5) - DB_PAGE_SIZE


async def test_get_all_users_excluded_edition_paginated_filter_name(database_session: AsyncSession):
    edition_a = models.Edition(year=2022, name="edA")
    edition_b = models.Edition(year=2023, name="edB")
    database_session.add(edition_a)
    database_session.add(edition_b)
    await database_session.commit()

    count = 0
    for i in range(round(DB_PAGE_SIZE * 1.5)):
        user_1 = models.User(name=f"User {i} - a", admin=False)
        user_2 = models.User(name=f"User {i} - b", admin=False)
        database_session.add(user_1)
        database_session.add(user_2)
        await database_session.commit()
        await database_session.execute(models.user_editions.insert(), [
            {"user_id": user_1.user_id, "edition_id": edition_a.edition_id},
            {"user_id": user_2.user_id, "edition_id": edition_b.edition_id},
        ])
        if "1" in str(i):
            count += 1
    await database_session.commit()

    a_users = await users_crud.get_users_filtered_page(database_session,
                                                       FilterParameters(page=0, exclude_edition="edB", name="1"))
    assert len(a_users) == min(count, DB_PAGE_SIZE)
    for user in a_users:
        assert "b" not in user.name
    assert len(await users_crud.get_users_filtered_page(database_session,
                                                        FilterParameters(page=1, exclude_edition="edB", name="1"))) == \
           max(count - DB_PAGE_SIZE, 0)

    b_users = await users_crud.get_users_filtered_page(database_session,
                                                       FilterParameters(page=0, exclude_edition="edA", name="1"))
    assert len(b_users) == min(count, DB_PAGE_SIZE)
    for user in b_users:
        assert "a" not in user.name
    assert len(await users_crud.get_users_filtered_page(database_session,
                                                        FilterParameters(page=1, exclude_edition="edA", name="1"))) == \
           max(count - DB_PAGE_SIZE, 0)


async def test_get_all_users_for_edition_excluded_edition_paginated(database_session: AsyncSession):
    edition_a = models.Edition(year=2022, name="edA")
    edition_b = models.Edition(year=2023, name="edB")
    database_session.add(edition_a)
    database_session.add(edition_b)
    await database_session.commit()

    correct_users = []
    for i in range(round(DB_PAGE_SIZE * 1.5)):
        user_1 = models.User(name=f"User {i} - a", admin=False)
        user_2 = models.User(name=f"User {i} - b", admin=False)
        database_session.add(user_1)
        database_session.add(user_2)
        await database_session.commit()
        await database_session.execute(models.user_editions.insert(), [
            {"user_id": user_1.user_id, "edition_id": edition_a.edition_id},
            {"user_id": user_2.user_id, "edition_id": edition_b.edition_id},
        ])
        if i % 2:
            await database_session.execute(models.user_editions.insert(), [
                {"user_id": user_1.user_id, "edition_id": edition_b.edition_id},
            ])
        else:
            correct_users.append(user_1)

    await database_session.commit()

    users = await users_crud.get_users_filtered_page(database_session, FilterParameters(page=0, exclude_edition="edB",
                                                                                        edition="edA"))
    assert len(users) == len(correct_users)
    for user in users:
        assert user in correct_users


async def test_edit_admin_status(database_session: AsyncSession):
    """Test changing the admin status of a user"""

    # Create user
    user = models.User(name="user1", admin=False)
    database_session.add(user)
    await database_session.commit()

    await users_crud.edit_admin_status(database_session, user.user_id, True)
    assert user.admin

    await users_crud.edit_admin_status(database_session, user.user_id, False)
    assert not user.admin


async def test_add_coach(database_session: AsyncSession):
    """Test adding a user as coach"""

    # Create user
    user = models.User(name="user1", admin=False)
    database_session.add(user)

    # Create edition
    edition = models.Edition(year=1, name="ed1")
    database_session.add(edition)

    await database_session.commit()
    await users_crud.add_coach(database_session, user.user_id, edition.name)
    coach = (await database_session.execute(select(user_editions))).one()
    assert coach.user_id == user.user_id
    assert coach.edition_id == edition.edition_id


async def test_remove_coach(database_session: AsyncSession):
    """Test removing a user as coach"""

    # Create user
    user1 = models.User(name="user1", admin=False)
    database_session.add(user1)
    user2 = models.User(name="user2", admin=False)
    database_session.add(user2)

    # Create edition
    edition = models.Edition(year=1, name="ed1")
    database_session.add(edition)

    await database_session.commit()

    # Create coach role
    await database_session.execute(models.user_editions.insert(), [
        {"user_id": user1.user_id, "edition_id": edition.edition_id},
        {"user_id": user2.user_id, "edition_id": edition.edition_id}
    ])

    await users_crud.remove_coach(database_session, user1.user_id, edition.name)
    assert len((await database_session.execute(select(user_editions))).scalars().all()) == 1


async def test_remove_coach_all_editions(database_session: AsyncSession):
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

    await database_session.commit()

    # Create coach role
    await database_session.execute(models.user_editions.insert(), [
        {"user_id": user1.user_id, "edition_id": edition1.edition_id},
        {"user_id": user1.user_id, "edition_id": edition2.edition_id},
        {"user_id": user1.user_id, "edition_id": edition3.edition_id},
        {"user_id": user2.user_id, "edition_id": edition2.edition_id},
    ])

    await users_crud.remove_coach_all_editions(database_session, user1.user_id)
    assert len((await database_session.execute(select(user_editions))).scalars().all()) == 1


async def test_get_all_requests(database_session: AsyncSession):
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

    await database_session.commit()

    # Create request
    request1 = models.CoachRequest(user_id=user1.user_id, edition_id=edition1.edition_id)
    request2 = models.CoachRequest(user_id=user2.user_id, edition_id=edition2.edition_id)
    database_session.add(request1)
    database_session.add(request2)

    await database_session.commit()

    requests = await users_crud.get_requests(database_session)
    assert len(requests) == 2
    assert request1 in requests
    assert request2 in requests
    users = [request.user for request in requests]
    assert user1 in users
    assert user2 in users


async def test_get_requests_paginated(database_session: AsyncSession):
    edition = models.Edition(year=2022, name="ed2022")
    database_session.add(edition)

    for i in range(round(DB_PAGE_SIZE * 1.5)):
        user = models.User(name=f"User {i}", admin=False)
        database_session.add(user)
        database_session.add(CoachRequest(user=user, edition=edition))
    await database_session.commit()

    assert len(await users_crud.get_requests_page(database_session, 0)) == DB_PAGE_SIZE
    assert len(await users_crud.get_requests_page(database_session, 1)) == round(
        DB_PAGE_SIZE * 1.5
    ) - DB_PAGE_SIZE


async def test_get_requests_paginated_filter_user_name(database_session: AsyncSession):
    edition = models.Edition(year=2022, name="ed2022")
    database_session.add(edition)

    count = 0
    for i in range(round(DB_PAGE_SIZE * 1.5)):
        user = models.User(name=f"User {i}", admin=False)
        database_session.add(user)
        database_session.add(CoachRequest(user=user, edition=edition))
        if "1" in str(i):
            count += 1
    await database_session.commit()

    assert len(await users_crud.get_requests_page(database_session, 0, "1")) == \
           min(DB_PAGE_SIZE, count)
    assert len(await users_crud.get_requests_page(database_session, 1, "1")) == \
           max(count - DB_PAGE_SIZE, 0)


async def test_get_all_requests_from_edition(database_session: AsyncSession):
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

    await database_session.commit()

    # Create request
    request1 = models.CoachRequest(user_id=user1.user_id, edition_id=edition1.edition_id)
    request2 = models.CoachRequest(user_id=user2.user_id, edition_id=edition2.edition_id)
    database_session.add(request1)
    database_session.add(request2)

    await database_session.commit()

    requests = await users_crud.get_requests_for_edition(database_session, edition1.name)
    assert len(requests) == 1
    assert requests[0].user == user1

    requests = await users_crud.get_requests_for_edition(database_session, edition2.name)
    assert len(requests) == 1
    assert requests[0].user == user2


async def test_get_requests_for_edition_paginated(database_session: AsyncSession):
    edition = models.Edition(year=2022, name="ed2022")
    database_session.add(edition)

    for i in range(round(DB_PAGE_SIZE * 1.5)):
        user = models.User(name=f"User {i}", admin=False)
        database_session.add(user)
        database_session.add(CoachRequest(user=user, edition=edition))
    await database_session.commit()

    assert len(await users_crud.get_requests_for_edition_page(database_session, edition.name, 0)) == DB_PAGE_SIZE
    assert len(await users_crud.get_requests_for_edition_page(database_session, edition.name, 1)) == round(
        DB_PAGE_SIZE * 1.5
    ) - DB_PAGE_SIZE


async def test_get_requests_for_edition_paginated_filter_user_name(database_session: AsyncSession):
    edition = models.Edition(year=2022, name="ed2022")
    database_session.add(edition)

    count = 0
    for i in range(round(DB_PAGE_SIZE * 1.5)):
        user = models.User(name=f"User {i}", admin=False)
        database_session.add(user)
        database_session.add(CoachRequest(user=user, edition=edition))
        if "1" in str(i):
            count += 1
    await database_session.commit()

    assert len(await users_crud.get_requests_for_edition_page(database_session, edition.name, 0, "1")) == \
           min(DB_PAGE_SIZE, count)
    assert len(await users_crud.get_requests_for_edition_page(database_session, edition.name, 1, "1")) == \
           max(count - DB_PAGE_SIZE, 0)


async def test_accept_request(database_session: AsyncSession):
    """Test accepting a coach request"""

    # Create user
    user1 = models.User(name="user1")
    database_session.add(user1)

    # Create edition
    edition1 = models.Edition(year=1, name="ed1")
    database_session.add(edition1)

    await database_session.commit()

    # Create request
    request1 = models.CoachRequest(user_id=user1.user_id, edition_id=edition1.edition_id)
    database_session.add(request1)

    await database_session.commit()

    await users_crud.accept_request(database_session, request1.request_id)

    requests = (await database_session.execute(select(CoachRequest))).scalars().all()
    assert len(requests) == 0

    assert user1.editions[0].edition_id == edition1.edition_id


async def test_reject_request_new_user(database_session: AsyncSession):
    """Test rejecting a coach request"""

    # Create user
    user1 = models.User(name="user1")
    database_session.add(user1)

    # Create edition
    edition1 = models.Edition(year=1, name="ed2022")
    database_session.add(edition1)
    await database_session.commit()

    # Create request
    request1 = models.CoachRequest(user_id=user1.user_id, edition_id=edition1.edition_id)
    database_session.add(request1)
    await database_session.commit()

    await users_crud.reject_request(database_session, request1.request_id)

    requests = (await database_session.execute(select(CoachRequest))).scalars().all()
    assert len(requests) == 0


async def test_remove_request_if_exists_exists(database_session: AsyncSession):
    """Test deleting a request when it exists"""
    user = models.User(name="user1")
    database_session.add(user)

    edition = models.Edition(year=2022, name="ed2022")
    database_session.add(edition)
    await database_session.commit()

    request = models.CoachRequest(user_id=user.user_id, edition_id=edition.edition_id)
    database_session.add(request)
    await database_session.commit()

    count = (await database_session.execute(select(func.count()).select_from(select(CoachRequest).subquery()))).scalar_one()
    assert count == 1

    # Remove the request
    await users_crud.remove_request_if_exists(database_session, user.user_id, edition.name)

    count = (
        await database_session.execute(select(func.count()).select_from(select(CoachRequest).subquery()))).scalar_one()
    assert count == 0


async def test_remove_request_if_not_exists(database_session: AsyncSession):
    """Test deleting a request when it doesn't exist"""
    user = models.User(name="user1")
    database_session.add(user)

    edition = models.Edition(year=2022, name="ed2022")
    database_session.add(edition)
    await database_session.commit()

    # Remove the request
    # If the test succeeds then it means no error was raised, even though the request
    # doesn't exist
    await users_crud.remove_request_if_exists(database_session, user.user_id, edition.name)
