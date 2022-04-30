import uuid

import pytest
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from src.app.exceptions.crud import DuplicateInsertException
from src.app.logic.register import create_request_email, create_request_github
from src.app.schemas.oauth.github import GitHubProfile
from src.app.schemas.register import EmailRegister
from src.database.models import AuthEmail, CoachRequest, User, Edition, InviteLink


async def test_create_request_email(database_session: AsyncSession):
    """Tests if a normal request can be created"""
    edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    invite_link: InviteLink = InviteLink(
        edition=edition, target_email="jw@gmail.com")
    database_session.add(invite_link)
    await database_session.commit()
    new_user = EmailRegister(name="jos", email="email@email.com",
                             pw="wachtwoord", uuid=invite_link.uuid)
    await create_request_email(database_session, new_user, edition)

    users = (await database_session.execute(select(User).where(User.name == "jos"))).unique().scalars().all()
    assert len(users) == 1
    coach_requests = (await database_session.execute(select(
        CoachRequest).where(CoachRequest.user == users[0]))).unique().scalars().all()
    auth_email = (await database_session.execute(select(AuthEmail).where(
        AuthEmail.user == users[0]))).scalars().all()
    assert len(coach_requests) == 1
    assert auth_email[0].pw_hash != new_user.pw
    assert len(auth_email) == 1


@pytest.mark.skip(reason="The async database rolls back both, even with nested query")
async def test_duplicate_user(database_session: AsyncSession):
    """Tests if there is a duplicate, it's not created in the database"""
    edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    invite_link1: InviteLink = InviteLink(
        edition=edition, target_email="jw@gmail.com")
    invite_link2: InviteLink = InviteLink(
        edition=edition, target_email="jw@gmail.com")
    database_session.add(invite_link1)
    database_session.add(invite_link2)
    await database_session.commit()
    nu1 = EmailRegister(name="user1", email="email@email.com",
                        pw="wachtwoord1", uuid=invite_link1.uuid)
    nu2 = EmailRegister(name="user2", email="email@email.com",
                        pw="wachtwoord2", uuid=invite_link2.uuid)

    # These two have to be nested transactions because they share the same database_session,
    # and otherwise the second one rolls the first one back
    # Making them nested transactions creates a savepoint so only that part is rolled back
    async with database_session.begin_nested():
        await create_request_email(database_session, nu1, edition)

    async with database_session.begin_nested():
        with pytest.raises(DuplicateInsertException):
            await create_request_email(database_session, nu2, edition)

    # Verify that second user wasn't added
    # the first addition was successful, the second wasn't
    users = (await database_session.execute(select(User))).unique().scalars().all()
    assert len(users) == 1
    assert users[0].name == nu1.name

    emails = (await database_session.execute(select(AuthEmail))).scalars().all()
    assert len(emails) == 1
    assert emails[0].user == users[0]

    requests = (await database_session.execute(select(CoachRequest))).unique().scalars().all()
    assert len(requests) == 1
    assert requests[0].user == users[0]

    # Verify that the link wasn't removed
    links = (await database_session.execute(select(InviteLink))).scalars().all()
    assert len(links) == 1


async def test_use_same_uuid_multiple_times(database_session: AsyncSession):
    """Tests that you can't use the same UUID multiple times"""
    edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    invite_link: InviteLink = InviteLink(
        edition=edition, target_email="jw@gmail.com")
    database_session.add(invite_link)
    await database_session.commit()
    new_user1 = EmailRegister(name="jos", email="email@email.com",
                              pw="wachtwoord", uuid=invite_link.uuid)
    await create_request_email(database_session, new_user1, edition)
    with pytest.raises(NoResultFound):
        new_user2 = EmailRegister(name="jos", email="email2@email.com",
                                  pw="wachtwoord", uuid=invite_link.uuid)
        await create_request_email(database_session, new_user2, edition)


async def test_not_a_correct_email(database_session: AsyncSession):
    """Tests when the email is not a correct email address, it gets the right error"""
    edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    await database_session.commit()
    with pytest.raises(ValidationError):
        new_user = EmailRegister(name="jos", email="email", pw="wachtwoord", uuid=uuid.uuid4())
        await create_request_email(database_session, new_user, edition)


async def test_create_request_github(database_session: AsyncSession):
    """Test creating a new request using GitHub OAuth"""
    edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    invite = InviteLink(edition=edition, target_email="a@b.c")
    database_session.add(invite)
    await database_session.commit()

    profile = GitHubProfile(access_token="", email="email@addre.ss", id=1, name="Name")
    await create_request_github(database_session, profile, invite.uuid, edition)

    users = database_session.query(User).where(User.name == "Name").all()

    assert len(users) == 1
    assert users[0].github_auth is not None
    assert users[0].github_auth.github_user_id == 1


async def test_create_request_github_duplicate(database_session: AsyncSession):
    """Test creating a request with an already-existing GitHub user"""
    edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    invite = InviteLink(edition=edition, target_email="a@b.c")
    database_session.add(invite)
    await database_session.commit()

    profile = GitHubProfile(access_token="", email="email@addre.ss", id=1, name="Name")
    await create_request_github(database_session, profile, invite.uuid, edition)

    users = database_session.query(User).where(User.name == "Name").all()

    assert len(users) == 1

    invite = InviteLink(edition=edition, target_email="a@b.c")
    database_session.add(invite)
    await database_session.commit()

    # Change everything but re-use the same GitHub userid
    profile.access_token = "another access token"
    profile.name = "another name"
    profile.email = "another@email.address"

    with pytest.raises(DuplicateInsertException):
        await create_request_github(database_session, profile, invite.uuid, edition)
