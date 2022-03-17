from sqlalchemy.orm import Session

from src.app.schemas.suggestion import NewSuggestion
from database.crud.suggestions import create_suggestion

def new_suggestion(db: Session, new_suggestion: NewSuggestion):
    pass