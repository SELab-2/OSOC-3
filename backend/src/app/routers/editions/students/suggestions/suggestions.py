from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from starlette import status
from src.app.routers.tags import Tags
from src.app.utils.dependencies import require_authorization, get_student, get_suggestion
from src.database.database import get_session
from src.database.models import Student, User, Suggestion
from src.app.logic.suggestions import make_new_suggestion, all_suggestions_of_student, remove_suggestion, change_suggestion
from src.app.schemas.suggestion import NewSuggestion, SuggestionListResponse, SuggestionResponse


students_suggestions_router = APIRouter(prefix="/suggestions", tags=[Tags.STUDENTS])


@students_suggestions_router.post("/", status_code=status.HTTP_201_CREATED, response_model=SuggestionResponse)
async def create_suggestion(new_suggestion: NewSuggestion, student: Student = Depends(get_student), db: Session = Depends(get_session), user: User = Depends(require_authorization)):
    """
    Make a suggestion about a student.
    """
    return make_new_suggestion(db, new_suggestion, user, student.student_id)

@students_suggestions_router.delete("/{suggestion_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_suggestion(db: Session = Depends(get_session), user: User = Depends(require_authorization), suggestion: Suggestion = Depends(get_suggestion)):
    """
    Delete a suggestion you made about a student.
    """
    remove_suggestion(db,suggestion,user)

@students_suggestions_router.put("/{suggestion_id}", status_code=status.HTTP_204_NO_CONTENT)
async def edit_suggestion(new_suggestion: NewSuggestion, student: Student = Depends(get_student), db: Session = Depends(get_session), user: User = Depends(require_authorization), suggestion: Suggestion = Depends(get_suggestion)):
    """
    Edit a suggestion you made about a student.
    """
    change_suggestion(db,new_suggestion,suggestion,user)

@students_suggestions_router.get("/", dependencies=[Depends(require_authorization)], status_code=status.HTTP_200_OK, response_model=SuggestionListResponse)
async def get_suggestion(student: Student = Depends(get_student), db: Session = Depends(get_session)):
    """
    Get all suggestions of a student.
    """
    return all_suggestions_of_student(db, student.student_id)
