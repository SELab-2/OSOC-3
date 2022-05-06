from sqlalchemy.ext.asyncio import AsyncSession
from tests.fill_database import fill_database

def test_fill_database(database_session: AsyncSession):
    """Test that fill_database don't give an error"""
    fill_database(database_session)
