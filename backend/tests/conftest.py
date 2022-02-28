"""Pytest configuration file with fixtures"""
from typing import Generator

import pytest

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from src.app import app
from src.database.database import get_session
from src.database.models import Base


@pytest.fixture(scope="session")
def database_engine() -> Engine:
    """Fixture to create an SQLite engine instead of MariaDB"""
    database_args = {
        "drivername": "sqlite",
        "database": "test.db"
    }

    # "check_same_thread: False" allows multiple connections at once to interact with the database
    # Only required for SQLite because it's a file
    return create_engine(URL.create(**database_args), connect_args={"check_same_thread": False})


@pytest.fixture(scope="session")
def tables(database_engine: Engine):
    """
    Fixture to initialize a database before the tests,
    and drop it again afterwards
    """
    Base.metadata.create_all(bind=database_engine)
    yield
    Base.metadata.drop_all(bind=database_engine)


@pytest.fixture
def database_session(database_engine: Engine, tables: None) -> Generator[Session, None, None]:
    """
    Fixture to create a session for every test, and rollback
    all the transactions so that each tests starts with a clean db
    """
    connection = database_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    # Clean up connections & rollback transactions
    session.close()
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
