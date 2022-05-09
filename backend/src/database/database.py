from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency to inject a database session into a route instead of using an import
    Allows the tests to replace it with another database session (not hard coding the session)
    """
    # Important: this is a LOCAL import so that
    # the tests never actually create a MariaDB engine connection!
    # DO NOT MOVE THIS IMPORT OUT OF THIS FUNCTION!
    from src.database.engine import DBSession

    session = DBSession()

    # Use "yield" and "finally" to close the session when it's no longer needed
    try:
        yield session
    finally:
        await session.close()
