from sqlalchemy.orm import Session

from src.app.schemas.suggestion import NewSuggestion
from src.database.crud.suggestions import create_suggestion, get_suggestions_of_student
from src.database.models import User
from src.app.schemas.suggestion import SuggestionListResponse

def make_new_suggestion(db: Session, new_suggestion: NewSuggestion, user: User, student_id: int):
    create_suggestion(db, user.user_id, student_id, new_suggestion.suggestion, new_suggestion.argumentation)

def all_suggestions_of_student(db: Session, student_id: int) -> SuggestionListResponse:
    suggestions_orm = get_suggestions_of_student(db, student_id)
    #return suggestions_orm
    return SuggestionListResponse(suggestions=suggestions_orm)
#def get_suggestions(db: )