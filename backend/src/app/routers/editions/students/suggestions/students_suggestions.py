from fastapi import APIRouter

from src.app.routers.tags import Tags

students_suggestions_router = APIRouter(prefix="/suggestions", tags=[Tags.STUDENTS])


@students_suggestions_router.post("/")
async def create_suggestion(edition_id: int, student_id: int):
    """
    Make a suggestion about a student.
    """


@students_suggestions_router.get("/{suggestion_id}")
async def delete_suggestion(edition_id: int, student_id: int, suggestion_id: int):
    """
    Delete a suggestion you made about a student.
    """


@students_suggestions_router.put("/{suggestion_id}")
async def edit_suggestion(edition_id: int, student_id: int, suggestion_id: int):
    """
    Edit a suggestion you made about a student.
    """
