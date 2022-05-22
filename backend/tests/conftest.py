"""Pytest configuration file with fixtures"""
from typing import AsyncGenerator, Generator
from unittest.mock import AsyncMock

import pytest
from alembic import command
from alembic import config
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.app import app
from src.app.utils.dependencies import get_http_session
from src.database.database import get_session
from src.database.engine import engine
from tests.utils.authorization import AuthClient


@pytest.fixture(scope="session")
def tables():
    """
    Fixture to initialize a database before the tests,
    and drop it again afterwards
    """
    alembic_config: config.Config = config.Config('alembic.ini')
    command.upgrade(alembic_config, 'head')
    yield
    command.downgrade(alembic_config, 'base')


@pytest.fixture
async def database_session(tables) -> AsyncGenerator[AsyncSession, None]:
    """
    Fixture to create a session for every test, and rollback
    all the transactions so that each tests starts with a clean db
    """
    connection = await engine.connect()
    transaction = await connection.begin()
    # AsyncSession needs expire_on_commit to be False
    session = AsyncSession(bind=connection, expire_on_commit=False)

    yield session

    # Clean up connections & rollback transactions
    await session.close()

    # Transactions can be invalidated when an exception is raised
    # which causes warnings when running the tests
    # Check if a transaction is still valid before rolling back
    if transaction.is_valid:
        await transaction.rollback()

    await connection.close()


@pytest.fixture
def aiohttp_session() -> AsyncMock:
    """Fixture to get a mock aiohttp.ClientSession instance
    Used to replace the dependency of the TestClient
    """
    yield AsyncMock()


@pytest.fixture
def test_client(database_session: AsyncSession, aiohttp_session: AsyncMock) -> AsyncClient:
    """Fixture to create a testing version of our main application"""

    def override_get_session() -> AsyncGenerator[AsyncSession, None]:
        """Inner function to override the Session used in the app
        A session provided by a fixture will be used instead
        """
        yield database_session

    def override_get_http_session() -> Generator[AsyncMock, None, None]:
        """Inner function to override the ClientSession used in the app"""
        yield aiohttp_session

    # Replace get_session with a call to this method instead
    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[get_http_session] = override_get_http_session
    return AsyncClient(app=app, base_url="http://test")


@pytest.fixture
def auth_client(database_session: AsyncSession, aiohttp_session: AsyncMock) -> AuthClient:
    """Fixture to get a TestClient that handles authentication"""

    def override_get_session() -> AsyncGenerator[AsyncSession, None]:
        """Inner function to override the Session used in the app
        A session provided by a fixture will be used instead
        """
        yield database_session

    def override_get_http_session() -> Generator[AsyncMock, None, None]:
        """Inner function to override the ClientSession used in the app"""
        yield aiohttp_session

    # Replace get_session with a call to this method instead
    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[get_http_session] = override_get_http_session
    return AuthClient(database_session, app=app, base_url="http://test")
