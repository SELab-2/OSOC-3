from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from starlette import status
from src.app.routers.tags import Tags
from src.app.utils.dependencies import get_edition, require_authorization
from src.database.database import get_session
from src.database.models import Edition, Student, User
from src.app.logic.suggestions import make_new_suggestion, get_suggestions_of_student
from src.app.schemas.suggestion import NewSuggestion


students_suggestions_router = APIRouter(prefix="/suggestions", tags=[Tags.STUDENTS])


@students_suggestions_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_suggestion(student_id: int, new_suggestion: NewSuggestion, db: Session = Depends(get_session), user: User = Depends(require_authorization)):
    """
    Make a suggestion about a student.
    """
    make_new_suggestion(db, new_suggestion, user, student_id)


@students_suggestions_router.get("/{suggestion_id}", dependencies=[Depends(require_authorization)], status_code=status.HTTP_200_OK)
async def get_suggestion(student_id: int, db: Session = Depends(get_session)):
    """
    Get all suggestions of a student.
    """
    return get_suggestions_of_student(db, student_id)


@students_suggestions_router.put("/{suggestion_id}", dependencies=[Depends(require_authorization)])
async def edit_suggestion(edition_id: int, student_id: int, suggestion_id: int):
    """
    Edit a suggestion you made about a student.
    """

@students_suggestions_router.delete("/{suggestion_id}", dependencies=[Depends(require_authorization)])
async def delete_suggestion(edition_id: int, suggestion_id: int):
    """
    Delete a suggestion you made about a student.
    """


#user: NewUser, db: Session = Depends(get_session), edition: Edition = Depends(get_edition)