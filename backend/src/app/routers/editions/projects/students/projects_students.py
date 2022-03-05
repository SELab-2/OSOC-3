from fastapi import APIRouter

from src.app.routers.tags import Tags

project_students_router = APIRouter(prefix="/students", tags=[Tags.PROJECTS, Tags.STUDENTS])


@project_students_router.delete("/{student_id}")
async def remove_student_from_project(edition_id: int, project_id: int, student_id: int):
    """
    Remove a student from a project.
    """


@project_students_router.patch("/{student_id}")
async def change_project_role(edition_id: int, project_id: int, student_id: int):
    """
    Change the role a student is drafted for in a project.
    """


@project_students_router.post("/{student_id}")
async def add_student_to_project(edition_id: int, project_id: int, student_id: int):
    """
    Add a student to a project.

    This is not a definitive decision, but represents a coach drafting the student.
    """
