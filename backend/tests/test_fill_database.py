from sqlalchemy.ext.asyncio import AsyncSession
from tests.fill_database import fill_database


async def test_fill_database(database_session: AsyncSession):
    """Test that fill_database don't give an error"""
    await fill_database(database_session)
