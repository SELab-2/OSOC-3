"""FastAPI TestClient to run tests against
Replaces the database connection with a local SQLite instance
"""
from typing import Generator

from starlette.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import Session, sessionmaker

from src.database.database import get_session
from src.database.models import Base
from src.app.app import app

# Connect to SQLite instead of MariaDB
DATABASE_ARGS = {
    "drivername": "sqlite",
    "database": "test.db"
}

# "check_same_thread: False" allows multiple connections at once to interact with the database
# Only required for SQLite
engine = create_engine(URL.create(**DATABASE_ARGS), connect_args={"check_same_thread": False})
TestSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Reset the local SQLite database
Base.metadata.drop_all(bind=engine)

# Initialize all tables
Base.metadata.create_all(bind=engine)


def override_get_session() -> Generator[Session, None, None]:
    """Replacement Session generator"""
    session = TestSession()

    try:
        yield session
    finally:
        session.close()


# Override Session dependency
app.dependency_overrides[get_session] = override_get_session


# Main testing client
client = TestClient(app)
