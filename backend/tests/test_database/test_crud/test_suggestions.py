from sqlalchemy.orm import Session

from src.database.models import Suggestion, Student, User

from src.database.crud.suggestions import create_suggestion
from tests.fill_database import fill_database

def test_create_suggestion(database_session: Session):
    fill_database(database_session)

    user: User = database_session.query(User).where(User.name == "coach1").first()
    print(user)

    assert False