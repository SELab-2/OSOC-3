from sqlalchemy.ext.asyncio import AsyncSession

from src.app.schemas.suggestion import NewSuggestion
from src.database.crud.suggestions import (
    create_suggestion, get_suggestions_of_student, get_own_suggestion, delete_suggestion, update_suggestion)
from src.database.models import Suggestion, User
from src.app.schemas.suggestion import SuggestionListResponse, SuggestionResponse, suggestion_model_to_schema
from src.app.exceptions.authentication import MissingPermissionsException


async def make_new_suggestion(db: AsyncSession, new_suggestion: NewSuggestion,
                              user: User, student_id: int | None) -> SuggestionResponse:
    """"Make a new suggestion"""
    own_suggestion = await get_own_suggestion(db, student_id, user.user_id)

    if own_suggestion is None:
        suggestion_orm = await create_suggestion(
            db, user.user_id, student_id, new_suggestion.suggestion, new_suggestion.argumentation)
    else:
        await update_suggestion(db, own_suggestion, new_suggestion.suggestion, new_suggestion.argumentation)
        suggestion_orm = own_suggestion

    suggestion = suggestion_model_to_schema(suggestion_orm)
    return SuggestionResponse(suggestion=suggestion)


async def all_suggestions_of_student(db: AsyncSession, student_id: int | None) -> SuggestionListResponse:
    """Get all suggestions of a student"""
    suggestions_orm = await get_suggestions_of_student(db, student_id)
    all_suggestions = []
    for suggestion in suggestions_orm:
        all_suggestions.append(suggestion_model_to_schema(suggestion))
    return SuggestionListResponse(suggestions=all_suggestions)


async def remove_suggestion(db: AsyncSession, suggestion: Suggestion, user: User) -> None:
    """
    Delete a suggestion
    Admins can delete all suggestions, coaches only their own suggestions
    """
    if user.admin or suggestion.coach == user:
        await delete_suggestion(db, suggestion)
    else:
        raise MissingPermissionsException


async def change_suggestion(db: AsyncSession, new_suggestion: NewSuggestion, suggestion: Suggestion,
                            user: User) -> None:
    """
    Update a suggestion
    Admins can update all suggestions, coaches only their own suggestions
    """
    if user.admin or suggestion.coach == user:
        await update_suggestion(
            db, suggestion, new_suggestion.suggestion, new_suggestion.argumentation)
    else:
        raise MissingPermissionsException
