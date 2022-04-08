from sqlalchemy.orm import Session

from src.app.schemas.suggestion import NewSuggestion
from src.database.crud.suggestions import create_suggestion, get_suggestions_of_student, delete_suggestion, update_suggestion
from src.database.models import Suggestion, User
from src.app.schemas.suggestion import SuggestionListResponse, SuggestionResponse, suggestion_model_to_schema
from src.app.exceptions.authentication import MissingPermissionsException


def make_new_suggestion(db: Session, new_suggestion: NewSuggestion, user: User, student_id: int) -> SuggestionResponse:
    """"Make a new suggestion"""
    suggestion_orm = create_suggestion(
        db, user.user_id, student_id, new_suggestion.suggestion, new_suggestion.argumentation)
    suggestion = suggestion_model_to_schema(suggestion_orm)
    return SuggestionResponse(suggestion=suggestion)



def all_suggestions_of_student(db: Session, student_id: int) -> SuggestionListResponse:
    """Get all suggestions of a student"""
    suggestions_orm = get_suggestions_of_student(db, student_id)
    all_suggestions = []
    for suggestion in suggestions_orm:
        all_suggestions.append(suggestion_model_to_schema(suggestion))
    return SuggestionListResponse(suggestions=all_suggestions)



def remove_suggestion(db: Session, suggestion: Suggestion, user: User) -> None:
    """
    Delete a suggestion
    Admins can delete all suggestions, coaches only their own suggestions
    """
    if user.admin:
        delete_suggestion(db, suggestion)
    elif suggestion.coach == user:
        delete_suggestion(db, suggestion)
    else:
        raise MissingPermissionsException


def change_suggestion(db: Session, new_suggestion: NewSuggestion, suggestion: Suggestion, user: User) -> None:
    """
    Update a suggestion
    Admins can update all suggestions, coaches only their own suggestions
    """
    if user.admin:
        update_suggestion(
            db, suggestion, new_suggestion.suggestion, new_suggestion.argumentation)
    elif suggestion.coach == user:
        update_suggestion(
            db, suggestion, new_suggestion.suggestion, new_suggestion.argumentation)
    else:
        raise MissingPermissionsException
