from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.schemas.oauth.github import GitHubProfile
from src.database.crud.register import create_user, create_coach_request, create_auth_email, create_auth_github
from src.database.models import AuthEmail, CoachRequest, User, Edition, AuthGitHub


async def test_create_user(database_session: AsyncSession):
    """Tests for creating a user"""
    await create_user(database_session, "jos")

    a = (await database_session.execute(select(User).where(User.name == "jos"))).unique().scalars().all()
    assert len(a) == 1
    assert a[0].name == "jos"


async def test_react_coach_request(database_session: AsyncSession):
    """Tests for creating a coach request"""
    edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    await database_session.commit()
    u = await create_user(database_session, "jos")
    await create_coach_request(database_session, u, edition)
    a = (await database_session.execute(select(CoachRequest).where(CoachRequest.user == u))).unique().scalars().all()

    assert len(a) == 1
    assert a[0].user_id == u.user_id
    assert u.coach_request == a[0]


async def test_create_auth_email(database_session: AsyncSession):
    """Tests for creating a auth email"""
    u = await create_user(database_session, "jos")
    await create_auth_email(database_session, u, "wachtwoord", "mail@email.com")

    a = (await database_session.execute(select(AuthEmail).where(AuthEmail.user == u))).scalars().all()

    assert len(a) == 1
    assert a[0].user_id == u.user_id
    assert a[0].pw_hash == "wachtwoord"
    assert u.email_auth == a[0]


async def test_create_auth_github(database_session: AsyncSession):
    """Test creating a GitHub auth entry"""
    user = await create_user(database_session, name="GitHub")
    profile = GitHubProfile(access_token="token", email="some@test.email", id=1, name="ghn")
    await create_auth_github(database_session, user, profile)

    a = (await database_session.execute(select(AuthGitHub).where(AuthGitHub.user == user))).scalars().all()

    assert len(a) == 1
    assert a[0].user_id == user.user_id
