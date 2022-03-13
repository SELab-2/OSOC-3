"""Pytest configuration file with fixtures"""
from typing import Generator

import pytest
from alembic import command
from alembic import config
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from src.app import app
from src.database.database import get_session
from src.database.engine import engine


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
def db(tables: None) -> Generator[Session, None, None]:
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
    transaction.rollback()
    connection.close()


@pytest.fixture
def test_client(db) -> TestClient:
    """Fixture to create a testing version of our main application"""

    def override_get_session() -> Generator[Session, None, None]:
        """Inner function to override the Session used in the app
        A session provided by a fixture will be used instead
        """
        yield db

    # Replace get_session with a call to this method instead
    app.dependency_overrides[get_session] = override_get_session
    return TestClient(app)
