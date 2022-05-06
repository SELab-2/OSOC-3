from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.testclient import TestClient


from src.database.models import Edition, InviteLink, User, AuthEmail


def test_ok(database_session: AsyncSession, test_client: TestClient):
    """Tests a registeration is made"""
    edition: Edition = Edition(year=2022, name="ed2022")
    invite_link: InviteLink = InviteLink(
        edition=edition, target_email="jw@gmail.com")
    database_session.add(edition)
    database_session.add(invite_link)
    database_session.commit()
    response = test_client.post("/editions/ed2022/register/email", json={
                                "name": "Joskes vermeulen", "email": "jw@gmail.com", "pw": "test",
                                "uuid": str(invite_link.uuid)})
    assert response.status_code == status.HTTP_201_CREATED
    user: User = database_session.query(User).where(
        User.name == "Joskes vermeulen").one()
    user_auth: AuthEmail = database_session.query(AuthEmail).where(AuthEmail.email == "jw@gmail.com").one()
    assert user.user_id == user_auth.user_id


def test_use_uuid_multiple_times(database_session: AsyncSession, test_client: TestClient):
    """Tests that you can't use the same UUID multiple times"""
    edition: Edition = Edition(year=2022, name="ed2022")
    invite_link: InviteLink = InviteLink(
        edition=edition, target_email="jw@gmail.com")
    database_session.add(edition)
    database_session.add(invite_link)
    database_session.commit()
    test_client.post("/editions/ed2022/register/email", json={
        "name": "Joskes vermeulen", "email": "jw@gmail.com", "pw": "test",
        "uuid": str(invite_link.uuid)})
    response = test_client.post("/editions/ed2022/register/email", json={
                                "name": "Joske Vermeulen", "email": "jw2@gmail.com", "pw": "test",
                                "uuid": str(invite_link.uuid)})
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_no_valid_uuid(database_session: AsyncSession, test_client: TestClient):
    """Tests that no valid uuid, can't make a account"""
    edition: Edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    database_session.commit()
    response = test_client.post("/editions/ed2022/register/email", json={
                                "name": "Joskes vermeulen", "email": "jw@gmail.com", "pw": "test",
                                "uuid": "550e8400-e29b-41d4-a716-446655440000"})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    users: list[User] = database_session.query(
        User).where(User.name == "Joskes vermeulen").all()
    assert len(users) == 0


def test_no_edition(database_session: AsyncSession, test_client: TestClient):
    """Tests if there is no edition it gets the right error code"""
    response = test_client.post("/editions/ed2022/register/email", json={
                                "name": "Joskes vermeulen", "email": "jw@gmail.com", "pw": "test"})
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_not_a_correct_email(database_session: AsyncSession, test_client: TestClient):
    """Tests when the email isn't correct, it gets the right error code"""
    database_session.add(Edition(year=2022, name="ed2022"))
    database_session.commit()
    response = test_client.post("/editions/ed2022/register/email",
                                json={"name": "Joskes vermeulen", "email": "jw", "pw": "test"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_duplicate_user(database_session: AsyncSession, test_client: TestClient):
    """Tests when there is a duplicate, it gets the right error code"""
    edition: Edition = Edition(year=2022, name="ed2022")
    invite_link1: InviteLink = InviteLink(
        edition=edition, target_email="jw@gmail.com")
    invite_link2: InviteLink = InviteLink(
        edition=edition, target_email="jw@gmail.com")
    database_session.add(edition)
    database_session.add(invite_link1)
    database_session.add(invite_link2)
    database_session.commit()
    test_client.post("/editions/ed2022/register/email",
                     json={"name": "Joskes vermeulen", "email": "jw@gmail.com", "pw": "test",
                           "uuid": str(invite_link1.uuid)})
    response = test_client.post("/editions/ed2022/register/email", json={
                                "name": "Joske vermeulen", "email": "jw@gmail.com", "pw": "test1",
                                "uuid": str(invite_link2.uuid)})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_old_edition(database_session: AsyncSession, test_client: TestClient):
    """Tests trying to make a registration for a read-only edition"""
    edition: Edition = Edition(year=2022, name="ed2022")
    edition3: Edition = Edition(year=2023, name="ed2023")
    invite_link: InviteLink = InviteLink(
        edition=edition, target_email="jw@gmail.com")
    database_session.add(edition)
    database_session.add(edition3)
    database_session.add(invite_link)
    database_session.commit()
    response = test_client.post("/editions/ed2022/register/email", json={
                                "name": "Joskes vermeulen", "email": "jw@gmail.com", "pw": "test",
                                "uuid": str(invite_link.uuid)})
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
