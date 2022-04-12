from json import dumps

import pytest
from sqlalchemy.orm import Session

from starlette import status

from settings import DB_PAGE_SIZE
from src.database import models
from src.database.models import user_editions, CoachRequest
from tests.utils.authorization import AuthClient


@pytest.fixture
def data(database_session: Session) -> dict[str, str | int]:
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
            "email1": email_auth1.email,
            "email2": github_auth1.email,
            "auth_type1": "email",
            "auth_type2": "github"
            }


def test_get_all_users(database_session: Session, auth_client: AuthClient, data: dict[str, str | int]):
    """Test endpoint for getting a list of users"""
    auth_client.admin()
    # All users
    response = auth_client.get("/users")
    assert response.status_code == status.HTTP_200_OK
    user_ids = [user["userId"] for user in response.json()['users']]
    user_ids.remove(auth_client.user.user_id)
    assert len(user_ids) == 2
    assert data["user1"] in user_ids
    assert data["user2"] in user_ids


def test_get_all_users_paginated(database_session: Session, auth_client: AuthClient):
    """Test endpoint for getting a list of users"""
    for i in range(round(DB_PAGE_SIZE * 1.5)):
        database_session.add(models.User(name=f"User {i}", admin=False))
    database_session.commit()

    auth_client.admin()
    response = auth_client.get("/users?page=0")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['users']) == DB_PAGE_SIZE
    response = auth_client.get("/users?page=1")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['users']) == round(DB_PAGE_SIZE * 1.5) - DB_PAGE_SIZE + 1
    # +1 because Authclient.admin() also creates one user.


def test_get_all_users_paginated_filter_name(database_session: Session, auth_client: AuthClient):
    """Test endpoint for getting a list of users with filter for name"""
    count = 0
    for i in range(round(DB_PAGE_SIZE * 1.5)):
        database_session.add(models.User(name=f"User {i}", admin=False))
        if "1" in str(i):
            count += 1
    database_session.commit()

    auth_client.admin()
    response = auth_client.get("/users?page=0&name=1")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['users']) == min(DB_PAGE_SIZE, count)
    response = auth_client.get("/users?page=1&name=1")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['users']) == max(count - round(DB_PAGE_SIZE * 1.5) - DB_PAGE_SIZE, 0)


def test_get_users_response(database_session: Session, auth_client: AuthClient, data: dict[str, str]):
    """Test the response model of a user"""
    auth_client.admin()
    response = auth_client.get("/users")
    users = response.json()["users"]
    user1 = [user for user in users if user["userId"] == data["user1"]][0]
    assert user1["auth"]["email"] == data["email1"]
    assert user1["auth"]["authType"] == data["auth_type1"]
    user2 = [user for user in users if user["userId"] == data["user2"]][0]
    assert user2["auth"]["email"] == data["email2"]
    assert user2["auth"]["authType"] == data["auth_type2"]


def test_get_all_admins(database_session: Session, auth_client: AuthClient, data: dict[str, str | int]):
    """Test endpoint for getting a list of admins"""
    auth_client.admin()
    # All admins
    response = auth_client.get("/users?admin=true")
    assert response.status_code == status.HTTP_200_OK
    user_ids = [user["userId"] for user in response.json()['users']]
    user_ids.remove(auth_client.user.user_id)
    assert [data["user1"]] == user_ids


def test_get_all_admins_paginated(database_session: Session, auth_client: AuthClient):
    """Test endpoint for getting a list of paginated admins"""
    count = 0
    for i in range(round(DB_PAGE_SIZE * 3)):
        database_session.add(models.User(name=f"User {i}", admin=i % 2 == 0))
        if i % 2 == 0:
            count += 1
    database_session.commit()

    auth_client.admin()
    response = auth_client.get("/users?admin=true&page=0")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['users']) == min(count + 1, DB_PAGE_SIZE)
    response = auth_client.get("/users?admin=true&page=1")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['users']) == min(count - DB_PAGE_SIZE + 1, DB_PAGE_SIZE + 1)
    # +1 because Authclient.admin() also creates one user.


def test_get_all_admins_paginated_filter_name(database_session: Session, auth_client: AuthClient):
    """Test endpoint for getting a list of paginated admins with filter for name"""
    for i in range(round(DB_PAGE_SIZE * 1.5)):
        database_session.add(models.User(name=f"User {i}", admin=True))
    database_session.commit()

    auth_client.admin()
    response = auth_client.get("/users?admin=true&page=0")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['users']) == DB_PAGE_SIZE
    response = auth_client.get("/users?admin=true&page=1")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['users']) == round(DB_PAGE_SIZE * 1.5) - DB_PAGE_SIZE + 1


def test_get_users_from_edition(database_session: Session, auth_client: AuthClient, data: dict[str, str | int]):
    """Test endpoint for getting a list of users from a given edition"""
    auth_client.admin()
    # All users from edition
    response = auth_client.get(f"/users?edition={data['edition2']}")
    assert response.status_code == status.HTTP_200_OK
    user_ids = [user["userId"] for user in response.json()['users']]
    assert [data["user2"]] == user_ids


def test_get_all_users_for_edition_paginated(database_session: Session, auth_client: AuthClient):
    """Test endpoint for getting a list of users"""
    edition = models.Edition(year=2022, name="ed2022")
    database_session.add(edition)

    for i in range(round(DB_PAGE_SIZE * 1.5)):
        database_session.add(models.User(name=f"User {i}", admin=False, editions=[edition]))
    database_session.commit()

    auth_client.admin()
    response = auth_client.get("/users?page=0&edition_name=ed2022")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['users']) == DB_PAGE_SIZE
    response = auth_client.get("/users?page=1&edition_name=ed2022")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['users']) == round(DB_PAGE_SIZE * 1.5) - DB_PAGE_SIZE + 1
    # +1 because Authclient.admin() also creates one user.


def test_get_all_users_for_edition_paginated_filter_user(database_session: Session, auth_client: AuthClient):
    """Test endpoint for getting a list of users and filter on name"""
    edition = models.Edition(year=2022, name="ed2022")
    database_session.add(edition)

    count = 0
    for i in range(round(DB_PAGE_SIZE * 1.5)):
        database_session.add(models.User(name=f"User {i}", admin=False, editions=[edition]))
        if "1" in str(i):
            count += 1
    database_session.commit()

    auth_client.admin()
    response = auth_client.get("/users?page=0&edition_name=ed2022&name=1")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['users']) == min(count , DB_PAGE_SIZE)
    response = auth_client.get("/users?page=1&edition_name=ed2022&name=1")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['users']) == max(count - DB_PAGE_SIZE, 0)


def test_get_admins_from_edition(database_session: Session, auth_client: AuthClient, data: dict[str, str | int]):
    """Test endpoint for getting a list of admins, edition should be ignored"""
    auth_client.admin()
    # All admins from edition
    response = auth_client.get(f"/users?admin=true&edition={data['edition1']}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['users']) == 2

    response = auth_client.get(f"/users?admin=true&edition={data['edition2']}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['users']) == 2


def test_get_all_users_excluded_edition_paginated(database_session: Session, auth_client: AuthClient):
    auth_client.admin()
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

    a_users = auth_client.get(f"/users?page=0&exclude_edition=edB").json()["users"]
    assert len(a_users) == DB_PAGE_SIZE
    for user in a_users:
        assert "b" not in user["name"]
    assert len(auth_client.get(f"/users?page=1&exclude_edition=edB").json()["users"]) == \
           round(DB_PAGE_SIZE * 1.5) - DB_PAGE_SIZE + 1  # auth_client is not a coach

    b_users = auth_client.get(f"/users?page=0&exclude_edition=edA").json()["users"]
    assert len(b_users) == DB_PAGE_SIZE
    for user in b_users:
        assert "a" not in user["name"]
    assert len(auth_client.get(f"/users?page=1&exclude_edition=edA").json()["users"]) == \
           round(DB_PAGE_SIZE * 1.5) - DB_PAGE_SIZE + 1  # auth_client is not a coach


def test_get_all_users_excluded_edition_paginated_filter_name(database_session: Session, auth_client: AuthClient):
    auth_client.admin()
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

    a_users = auth_client.get(f"/users?page=0&exclude_edition=edB&name=1").json()["users"]
    assert len(a_users) == min(count, DB_PAGE_SIZE)
    for user in a_users:
        assert "b" not in user["name"]
    assert len(auth_client.get(f"/users?page=1&exclude_edition=edB&name=1").json()["users"]) == \
           max(count - DB_PAGE_SIZE, 0)

    b_users = auth_client.get(f"/users?page=0&exclude_edition=edA&name=1").json()["users"]
    assert len(b_users) == min(count, DB_PAGE_SIZE)
    for user in b_users:
        assert "a" not in user["name"]
    assert len(auth_client.get(f"/users?page=1&exclude_edition=edA&name=1").json()["users"]) == \
           max(count - DB_PAGE_SIZE, 0)


def test_get_all_users_for_edition_excluded_edition_paginated(database_session: Session, auth_client: AuthClient):
    auth_client.admin()
    edition_a = models.Edition(year=2022, name="edA")
    edition_b = models.Edition(year=2023, name="edB")
    database_session.add(edition_a)
    database_session.add(edition_b)
    database_session.commit()

    correct_users_id = []
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
            correct_users_id.append(user_1.user_id)

    database_session.commit()

    users = auth_client.get(f"/users?page=0&exclude_edition=edB&edition=edA").json()["users"]
    assert len(users) == len(correct_users_id)
    for user in users:
        assert user["userId"] in correct_users_id


def test_get_users_invalid(database_session: Session, auth_client: AuthClient, data: dict[str, str | int]):
    """Test endpoint for unvalid input"""
    auth_client.admin()
    # Invalid input
    response = auth_client.get("/users?admin=INVALID")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_edit_admin_status(database_session: Session, auth_client: AuthClient):
    """Test endpoint for editing the admin status of a user"""
    auth_client.admin()
    # Create user
    user = models.User(name="user1", admin=False)
    database_session.add(user)
    database_session.commit()

    response = auth_client.patch(f"/users/{user.user_id}",
                                 data=dumps({"admin": True}))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert user.admin

    response = auth_client.patch(f"/users/{user.user_id}",
                                 data=dumps({"admin": False}))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not user.admin


def test_add_coach(database_session: Session, auth_client: AuthClient):
    """Test endpoint for adding coaches"""
    auth_client.admin()
    # Create user
    user = models.User(name="user1", admin=False)
    database_session.add(user)

    # Create edition
    edition = models.Edition(year=1, name="ed1")
    database_session.add(edition)

    database_session.commit()

    # Add coach
    response = auth_client.post(f"/users/{user.user_id}/editions/{edition.name}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    coach = database_session.query(user_editions).one()
    assert coach.user_id == user.user_id
    assert coach.edition_id == edition.edition_id


def test_remove_coach(database_session: Session, auth_client: AuthClient):
    """Test endpoint for removing coaches"""
    auth_client.admin()
    # Create user
    user = models.User(name="user1")
    database_session.add(user)

    # Create edition
    edition = models.Edition(year=1, name="ed1")
    database_session.add(edition)

    database_session.commit()

    # Create request
    request = models.CoachRequest(user_id=user.user_id, edition_id=edition.edition_id)
    database_session.add(request)

    database_session.commit()

    # Remove coach
    response = auth_client.delete(f"/users/{user.user_id}/editions/{edition.name}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    coach = database_session.query(user_editions).all()
    assert len(coach) == 0


def test_remove_coach_all_editions(database_session: Session, auth_client: AuthClient):
    """Test removing a user as coach from all editions"""
    auth_client.admin()

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

    response = auth_client.delete(f"/users/{user1.user_id}/editions")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    coach = database_session.query(user_editions).all()
    assert len(coach) == 1


def test_get_all_requests(database_session: Session, auth_client: AuthClient):
    """Test endpoint for getting all userrequests"""
    auth_client.admin()

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

    response = auth_client.get("/users/requests")
    assert response.status_code == status.HTTP_200_OK
    user_ids = [request["user"]["userId"] for request in response.json()['requests']]
    assert len(user_ids) == 2
    assert user1.user_id in user_ids
    assert user2.user_id in user_ids


def test_get_all_requests_paginated(database_session: Session, auth_client: AuthClient):
    """Test endpoint for getting a paginated list of requests"""
    edition = models.Edition(year=2022, name="ed2022")

    for i in range(round(DB_PAGE_SIZE * 1.5)):
        user = models.User(name=f"User {i}", admin=False)
        database_session.add(user)
        database_session.add(models.CoachRequest(user=user, edition=edition))
    database_session.commit()

    auth_client.admin()
    response = auth_client.get("/users/requests?page=0")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['requests']) == DB_PAGE_SIZE
    response = auth_client.get("/users/requests?page=1")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['requests']) == round(DB_PAGE_SIZE * 1.5) - DB_PAGE_SIZE


def test_get_all_requests_paginated_filter_name(database_session: Session, auth_client: AuthClient):
    """Test endpoint for getting a paginated list of requests"""
    edition = models.Edition(year=2022, name="ed2022")

    count = 0
    for i in range(round(DB_PAGE_SIZE * 1.5)):
        user = models.User(name=f"User {i}", admin=False)
        database_session.add(user)
        database_session.add(models.CoachRequest(user=user, edition=edition))
        if "1" in str(i):
            count += 1
    database_session.commit()

    auth_client.admin()
    response = auth_client.get("/users/requests?page=0&user=1")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['requests']) == min(DB_PAGE_SIZE, count)
    response = auth_client.get("/users/requests?page=1&user=1")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['requests']) ==  max(count-DB_PAGE_SIZE, 0)


def test_get_all_requests_from_edition(database_session: Session, auth_client: AuthClient):
    """Test endpoint for getting all userrequests of a given edition"""
    auth_client.admin()

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

    response = auth_client.get(f"/users/requests?edition={edition1.name}")
    assert response.status_code == status.HTTP_200_OK
    requests = response.json()['requests']
    assert len(requests) == 1
    assert user1.user_id == requests[0]["user"]["userId"]

    response = auth_client.get(f"/users/requests?edition={edition2.name}")
    assert response.status_code == status.HTTP_200_OK
    requests = response.json()['requests']
    assert len(requests) == 1
    assert user2.user_id == requests[0]["user"]["userId"]


def test_get_all_requests_for_edition_paginated(database_session: Session, auth_client: AuthClient):
    """Test endpoint for getting a paginated list of requests"""
    edition = models.Edition(year=2022, name="ed2022")

    for i in range(round(DB_PAGE_SIZE * 1.5)):
        user = models.User(name=f"User {i}", admin=False)
        database_session.add(user)
        database_session.add(models.CoachRequest(user=user, edition=edition))
    database_session.commit()

    auth_client.admin()
    response = auth_client.get("/users/requests?page=0&edition_name=ed2022")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['requests']) == DB_PAGE_SIZE
    response = auth_client.get("/users/requests?page=1&edition_name=ed2022")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['requests']) == round(DB_PAGE_SIZE * 1.5) - DB_PAGE_SIZE


def test_get_all_requests_for_edition_paginated_filter_name(database_session: Session, auth_client: AuthClient):
    """Test endpoint for getting a paginated list of requests"""
    edition = models.Edition(year=2022, name="ed2022")

    count = 0
    for i in range(round(DB_PAGE_SIZE * 1.5)):
        user = models.User(name=f"User {i}", admin=False)
        database_session.add(user)
        database_session.add(models.CoachRequest(user=user, edition=edition))
        if "1" in str(i):
            count += 1
    database_session.commit()

    auth_client.admin()
    response = auth_client.get("/users/requests?page=0&edition_name=ed2022&user=1")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['requests']) == min(DB_PAGE_SIZE, count)
    response = auth_client.get("/users/requests?page=1&edition_name=ed2022&user=1")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['requests']) == max(count-DB_PAGE_SIZE, 0)


def test_accept_request(database_session, auth_client: AuthClient):
    """Test endpoint for accepting a coach request"""
    auth_client.admin()
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

    response = auth_client.post(f"users/requests/{request1.request_id}/accept")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert len(user1.editions) == 1
    assert user1.editions[0].edition_id == edition1.edition_id


def test_reject_request(database_session, auth_client: AuthClient):
    """Test endpoint for rejecting a coach request"""
    auth_client.admin()
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

    response = auth_client.post(f"users/requests/{request1.request_id}/reject")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    requests = database_session.query(CoachRequest).all()
    assert len(requests) == 0

    response = auth_client.post("users/requests/INVALID/reject")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
