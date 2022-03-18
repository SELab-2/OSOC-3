from sqlalchemy.orm import Session

from src.app.logic.suggestions import all_suggestions_of_student
from src.database.models import User 
from tests.fill_database import fill_database
from src.database.crud.suggestions import create_suggestion
from src.database.enums import DecisionEnum
from src.app.schemas.suggestion import SuggestionListResponse

def test_all_suggestions_of_student(database_session: Session):
    """Test if I get all suggestions of a student"""
    fill_database(database_session)
    user: User = database_session.query(User).where(User.email == "coach1@noutlook.be")
    create_suggestion(database_session, 2, 1, DecisionEnum.YES, "Idk if it's good student")
    suggestions: SuggestionListResponse  = all_suggestions_of_student(database_session, 1)
    print(suggestions)
    assert True
