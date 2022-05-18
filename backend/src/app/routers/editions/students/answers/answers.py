from fastapi import APIRouter, Depends

from starlette import status
from src.app.logic.answers import gives_question_and_answers
from src.app.routers.tags import Tags
from src.app.utils.dependencies import get_student, require_coach
from src.app.schemas.answers import Questions
from src.database.models import Student

students_answers_router = APIRouter(
    prefix="/answers", tags=[Tags.STUDENTS])


@students_answers_router.get("/", status_code=status.HTTP_200_OK, response_model=Questions,
                             dependencies=[Depends(require_coach)])
async def get_answers(student: Student = Depends(get_student)):
    """give answers of a student"""
    return await gives_question_and_answers(student=student)
