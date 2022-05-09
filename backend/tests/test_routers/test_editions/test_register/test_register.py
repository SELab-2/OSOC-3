from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.testclient import TestClient


from src.database.models import Edition, InviteLink, User, AuthEmail


async def test_ok(database_session: AsyncSession, test_client: AsyncClient):
    """Tests a registeration is made"""
    edition: Edition = Edition(year=2022, name="ed2022")
    invite_link: InviteLink = InviteLink(
        edition=edition, target_email="jw@gmail.com")
    database_session.add(edition)
    database_session.add(invite_link)
    await database_session.commit()
    async with test_client:
        response = await test_client.post("/editions/ed2022/register/email", json={
                                    "name": "Joskes vermeulen", "email": "jw@gmail.com", "pw": "test",
                                    "uuid": str(invite_link.uuid)})
        assert response.status_code == status.HTTP_201_CREATED
        user: User = (await database_session.execute(select(User).where(
            User.name == "Joskes vermeulen"))).unique().scalar_one()
        user_auth: AuthEmail = (await database_session.execute(select(AuthEmail).where(AuthEmail.email == "jw@gmail.com"))).scalar_one()
        assert user.user_id == user_auth.user_id


async def test_use_uuid_multiple_times(database_session: AsyncSession, test_client: AsyncClient):
    """Tests that you can't use the same UUID multiple times"""
    edition: Edition = Edition(year=2022, name="ed2022")
    invite_link: InviteLink = InviteLink(
        edition=edition, target_email="jw@gmail.com")
    database_session.add(edition)
    database_session.add(invite_link)
    await database_session.commit()
    async with test_client:
        await test_client.post("/editions/ed2022/register/email", json={
            "name": "Joskes vermeulen", "email": "jw@gmail.com", "pw": "test",
            "uuid": str(invite_link.uuid)})
        response = await test_client.post("/editions/ed2022/register/email", json={
                                    "name": "Joske Vermeulen", "email": "jw2@gmail.com", "pw": "test",
                                    "uuid": str(invite_link.uuid)})
        assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_no_valid_uuid(database_session: AsyncSession, test_client: AsyncClient):
    """Tests that no valid uuid, can't make a account"""
    edition: Edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    await database_session.commit()
    async with test_client:
        response = await test_client.post("/editions/ed2022/register/email", json={
                                    "name": "Joskes vermeulen", "email": "jw@gmail.com", "pw": "test",
                                    "uuid": "550e8400-e29b-41d4-a716-446655440000"})
        assert response.status_code == status.HTTP_404_NOT_FOUND
        users: list[User] = (await database_session.execute(select(
            User).where(User.name == "Joskes vermeulen"))).scalars().all()
        assert len(users) == 0


async def test_no_edition(database_session: AsyncSession, test_client: AsyncClient):
    """Tests if there is no edition it gets the right error code"""
    async with test_client:
        response = await test_client.post("/editions/ed2022/register/email", json={
                                    "name": "Joskes vermeulen", "email": "jw@gmail.com", "pw": "test"})
    assert response.status_code == status.HTTP_404_NOT_FOUND


async def test_not_a_correct_email(database_session: AsyncSession, test_client: AsyncClient):
    """Tests when the email isn't correct, it gets the right error code"""
    database_session.add(Edition(year=2022, name="ed2022"))
    await database_session.commit()
    async with test_client:
        response = await test_client.post("/editions/ed2022/register/email",
                                    json={"name": "Joskes vermeulen", "email": "jw", "pw": "test"})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_duplicate_user(database_session: AsyncSession, test_client: AsyncClient):
    """Tests when there is a duplicate, it gets the right error code"""
    edition: Edition = Edition(year=2022, name="ed2022")
    invite_link1: InviteLink = InviteLink(
        edition=edition, target_email="jw@gmail.com")
    invite_link2: InviteLink = InviteLink(
        edition=edition, target_email="jw@gmail.com")
    database_session.add(edition)
    database_session.add(invite_link1)
    database_session.add(invite_link2)
    await database_session.commit()
    async with test_client:
        await test_client.post("/editions/ed2022/register/email",
                         json={"name": "Joskes vermeulen", "email": "jw@gmail.com", "pw": "test",
                               "uuid": str(invite_link1.uuid)})
        response = await test_client.post("/editions/ed2022/register/email", json={
                                    "name": "Joske vermeulen", "email": "jw@gmail.com", "pw": "test1",
                                    "uuid": str(invite_link2.uuid)})
        assert response.status_code == status.HTTP_400_BAD_REQUEST


async def test_old_edition(database_session: AsyncSession, test_client: AsyncClient):
    """Tests trying to make a registration for a read-only edition"""
    edition: Edition = Edition(year=2022, name="ed2022")
    edition3: Edition = Edition(year=2023, name="ed2023")
    invite_link: InviteLink = InviteLink(
        edition=edition, target_email="jw@gmail.com")
    database_session.add(edition)
    database_session.add(edition3)
    database_session.add(invite_link)
    await database_session.commit()
    async with test_client:
        response = await test_client.post("/editions/ed2022/register/email", json={
                                    "name": "Joskes vermeulen", "email": "jw@gmail.com", "pw": "test",
                                    "uuid": str(invite_link.uuid)})
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
