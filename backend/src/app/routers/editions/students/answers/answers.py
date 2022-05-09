from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from starlette import status
from src.app.routers.tags import Tags
from src.app.utils.dependencies import get_student
from src.database.models import Student
from src.database.database import get_session

students_answers_router = APIRouter(
    prefix="/answers", tags=[Tags.STUDENTS])


@students_answers_router.get("/", status_code=status.HTTP_200_OK)
async def get_answers(student: Student = Depends(get_student),
                      db: AsyncSession = Depends(get_session)):
    """give answers of a student"""
    return student.alumni
