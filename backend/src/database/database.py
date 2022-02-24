from typing import Generator
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

import settings

# Urlencode the password to pass it to the engine
_encoded_password = quote_plus(settings.DB_PASSWORD)

database_url = f"mariadb+mariadbconnector://{settings.DB_USERNAME}:{_encoded_password}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

engine = create_engine(database_url)

DBSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session() -> Generator[Session, None, None]:
    """FastAPI dependency to inject a database session into a route instead of using an import
    Allows the tests to replace it with another database session (not hard coding the session)
    """
    session = DBSession()

    # Use "yield" and "finally" to close the session when it's no longer needed
    try:
        yield session
    finally:
        session.close()
