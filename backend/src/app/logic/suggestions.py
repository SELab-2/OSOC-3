from sqlalchemy.orm import Session

from src.app.schemas.suggestion import NewSuggestion
from src.database.crud.suggestions import create_suggestion, get_suggestions_of_student
from src.database.models import Suggestion, User

def make_new_suggestion(db: Session, new_suggestion: NewSuggestion, user: User, student_id: int):
    create_suggestion(db, user.user_id, student_id, new_suggestion.suggestion, new_suggestion.argumentation)

def all_suggestions_of_student(db: Session, student_id: int) -> list[Suggestion]:
    return get_suggestions_of_student(db, student_id)
#def get_suggestions(db: )