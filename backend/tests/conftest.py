"""Pytest configuration file with fixtures"""
from typing import Generator

import pytest
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from src.app import app
from src.database.database import get_session
from src.database.engine import engine
from src.database.models import Base
from tests.utils.authorization import AuthClient


# @pytest.fixture(scope="session")
# def tables():
#     """
#     Fixture to initialize a database before the tests,
#     and drop it again afterwards
#     """
#     alembic_config: config.Config = config.Config('alembic.ini')
#     command.upgrade(alembic_config, 'head')
#     yield
#     command.downgrade(alembic_config, 'base')


@pytest.fixture(scope="session")
def tables():
    """
    Fixture to initialize a database before the tests
    """
    Base.metadata.create_all(bind=engine)


@pytest.fixture
def database_session(tables) -> Generator[Session, None, None]:
    """
    Fixture to create a session for every test, and rollback
    all the transactions so that each tests starts with a clean db
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    # Clean up connections & rollback transactions
    session.close()

    # Transactions can be invalidated when an exception is raised
    # which causes warnings when running the tests
    # Check if a transaction is still valid before rolling back
    if transaction.is_valid:
        transaction.rollback()

    connection.close()


@pytest.fixture
def test_client(database_session: Session) -> TestClient:
    """Fixture to create a testing version of our main application"""

    def override_get_session() -> Generator[Session, None, None]:
        """Inner function to override the Session used in the app
        A session provided by a fixture will be used instead
        """
        yield database_session

    # Replace get_session with a call to this method instead
    app.dependency_overrides[get_session] = override_get_session
    return TestClient(app)


@pytest.fixture
def auth_client(database_session: Session) -> AuthClient:
    """Fixture to get a TestClient that handles authentication"""

    def override_get_session() -> Generator[Session, None, None]:
        """Inner function to override the Session used in the app
        A session provided by a fixture will be used instead
        """
        yield database_session

    # Replace get_session with a call to this method instead
    app.dependency_overrides[get_session] = override_get_session
    return AuthClient(database_session, app)
