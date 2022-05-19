from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import Response

import src.app.logic.projects_students as logic
from src.app.routers.tags import Tags
from src.app.schemas.projects import InputArgumentation, ReturnProjectRoleSuggestion
from src.app.utils.dependencies import (
    require_coach, get_latest_edition, get_student,
    get_project_role
)
from src.app.utils.websockets import live
from src.database.database import get_session
from src.database.models import User, Student, ProjectRole

project_students_router = APIRouter(prefix="/students", tags=[Tags.PROJECTS, Tags.STUDENTS])


@project_students_router.delete(
    "/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT, response_class=Response,
    dependencies=[Depends(require_coach), Depends(get_latest_edition), Depends(live)]
)
async def remove_student_from_project(
        student: Student = Depends(get_student),
        db: AsyncSession = Depends(get_session),
        project_role: ProjectRole = Depends(get_project_role)):
    """
    Remove a student from a project.
    """
    await logic.remove_project_role_suggestion(db, project_role, student)


@project_students_router.patch(
    "/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT, response_class=Response,
    dependencies=[Depends(get_latest_edition), Depends(live)]
)
async def change_project_role(
        argumentation: InputArgumentation,
        student: Student = Depends(get_student),
        db: AsyncSession = Depends(get_session),
        project_role: ProjectRole = Depends(get_project_role),
        user: User = Depends(require_coach)):
    """
    Change the role a student is drafted for in a project.
    """
    await logic.change_project_role_suggestion(db, project_role, student, user, argumentation)


@project_students_router.post(
    "/{student_id}",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_latest_edition), Depends(live)],
    response_model=ReturnProjectRoleSuggestion
)
async def add_student_to_project(
        argumentation: InputArgumentation,
        student: Student = Depends(get_student),
        db: AsyncSession = Depends(get_session),
        project_role: ProjectRole = Depends(get_project_role),
        user: User = Depends(require_coach)):
    """
    Add a student to a project.

    This is not a definitive decision, but represents a coach drafting the student.
    """
    return await logic.add_student_project(db, project_role, student, user, argumentation)
