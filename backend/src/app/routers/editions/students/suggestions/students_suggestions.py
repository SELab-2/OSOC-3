from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.app.routers.tags import Tags
from src.app.utils.dependencies import get_edition, require_authorization
from src.database.database import get_session
from src.database.models import Edition, User


students_suggestions_router = APIRouter(prefix="/suggestions", tags=[Tags.STUDENTS])


@students_suggestions_router.post("/")
async def create_suggestion(db: Session = Depends(get_session), edition: Edition = Depends(get_edition), user: User = Depends(require_authorization)):
    """
    Make a suggestion about a student.
    """
    return user


@students_suggestions_router.get("/{suggestion_id}")
async def get_suggestion(db: Session = Depends(get_session), edition: Edition = Depends(get_edition), user: User = Depends(require_authorization)):
    """
    Get all suggestions of a student.
    """
    #test_client.post("/editions/1/students/1/suggestions/")


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