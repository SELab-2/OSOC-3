from sqlalchemy.orm import Session
from tests.fill_database import fill_database

def test_fill_database(database_session: Session):
    """Test that fill_database don't give an error"""
    fill_database(database_session)
