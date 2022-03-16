from sqlalchemy.orm import Session

from src.database.models import Suggestion, Student, User

from src.database.crud.suggestions import create_suggestion