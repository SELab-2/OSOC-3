from sqlalchemy.orm import Session
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.testclient import TestClient

from src.app.logic import security
from src.database.models import AuthEmail, User


async def test_login_non_existing(test_client: AsyncClient):
    """Test logging in without an existing account"""
    form = {
        "username": "this user",
        "password": "does not exist"
    }
    async with test_client:
        assert (await test_client.post("/login/token/email", data=form)).status_code == status.HTTP_401_UNAUTHORIZED


async def test_login_existing(database_session: AsyncSession, test_client: AsyncClient):
    """Test logging in with an existing account"""
    email = "test@ema.il"
    password = "password"

    # Create new user & auth entries in db
    user = User(name="test")

    database_session.add(user)
    await database_session.commit()

    auth = AuthEmail(pw_hash=security.get_password_hash(password), email=email)
    auth.user = user
    database_session.add(auth)
    await database_session.commit()

    # Try to get a token using the credentials for the new user
    form = {
        "username": email,
        "password": password
    }
    async with test_client:
        assert (await test_client.post("/login/token/email", data=form)).status_code == status.HTTP_200_OK


async def test_login_existing_wrong_credentials(database_session: AsyncSession, test_client: AsyncClient):
    """Test logging in with existing, but wrong credentials"""
    email = "test@ema.il"
    password = "password"

    # Create new user & auth entries in db
    user = User(name="test")

    database_session.add(user)
    await database_session.commit()

    auth = AuthEmail(pw_hash=security.get_password_hash(password), email=email)
    auth.user = user
    database_session.add(auth)
    await database_session.commit()

    # Try to get a token using the credentials for the new user
    form = {
        "username": email,
        "password": "another password"
    }
    async with test_client:
        assert (await test_client.post("/login/token/email", data=form)).status_code == status.HTTP_401_UNAUTHORIZED

