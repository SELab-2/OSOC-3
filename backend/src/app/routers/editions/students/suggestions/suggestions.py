from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from starlette import status
from starlette.responses import Response

from src.app.routers.tags import Tags
from src.app.utils.dependencies import require_auth, get_student, get_suggestion
from src.app.utils.websockets import live
from src.database.database import get_session
from src.database.models import Student, User, Suggestion
from src.app.logic.suggestions import (make_new_suggestion, all_suggestions_of_student,
                                       remove_suggestion, change_suggestion)
from src.app.schemas.suggestion import NewSuggestion, SuggestionListResponse, SuggestionResponse


students_suggestions_router = APIRouter(
    prefix="/suggestions", tags=[Tags.STUDENTS])


@students_suggestions_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=SuggestionResponse,
    dependencies=[Depends(live)]
)
async def create_suggestion(new_suggestion: NewSuggestion, student: Student = Depends(get_student),
                            db: AsyncSession = Depends(get_session), user: User = Depends(require_auth)):
    """
    Make a suggestion about a student.

    In case you've already made a suggestion previously, this replaces the existing suggestion.
    This simplifies the process in frontend, so we can just send a new request without making an edit interface.
    """
    return await make_new_suggestion(db, new_suggestion, user, student.student_id)


@students_suggestions_router.delete(
    "/{suggestion_id}",
    status_code=status.HTTP_204_NO_CONTENT, response_class=Response,
    dependencies=[Depends(live)]
)
async def delete_suggestion(db: AsyncSession = Depends(get_session), user: User = Depends(require_auth),
                            suggestion: Suggestion = Depends(get_suggestion)):
    """
    Delete a suggestion you made about a student.
    """
    await remove_suggestion(db, suggestion, user)


@students_suggestions_router.put(
    "/{suggestion_id}",
    status_code=status.HTTP_204_NO_CONTENT, response_class=Response,
    dependencies=[Depends(get_student), Depends(live)]
)
async def edit_suggestion(new_suggestion: NewSuggestion, db: AsyncSession = Depends(get_session),
                          user: User = Depends(require_auth), suggestion: Suggestion = Depends(get_suggestion)):
    """
    Edit a suggestion you made about a student.
    """
    await change_suggestion(db, new_suggestion, suggestion, user)


@students_suggestions_router.get("", dependencies=[Depends(require_auth)],
                                 status_code=status.HTTP_200_OK, response_model=SuggestionListResponse)
async def get_suggestions(student: Student = Depends(get_student), db: AsyncSession = Depends(get_session)):
    """
    Get all suggestions of a student.
    """
    return await all_suggestions_of_student(db, student.student_id)
