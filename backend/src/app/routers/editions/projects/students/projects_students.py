from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import Response

from src.app.routers.tags import Tags
from src.app.schemas.projects import InputStudentRole
from src.app.utils.dependencies import get_project, require_coach
from src.database.database import get_session
from src.database.models import Project
from src.app.logic.projects_students import logic_remove_student_project, logic_add_student_project, \
    logic_change_project_role

project_students_router = APIRouter(prefix="/students", tags=[Tags.PROJECTS, Tags.STUDENTS])


@project_students_router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response, dependencies=[Depends(require_coach)])
async def remove_student_from_project(student_id: int, db: Session = Depends(get_session),
                                      project: Project = Depends(get_project)):
    """
    Remove a student from a project.
    """
    logic_remove_student_project(db, project, student_id)


@project_students_router.patch("/{student_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response, dependencies=[Depends(require_coach)])
async def change_project_role(student_id: int, input_sr: InputStudentRole, db: Session = Depends(get_session),
                              project: Project = Depends(get_project)):
    """
    Change the role a student is drafted for in a project.
    """
    logic_change_project_role(db, project, student_id, input_sr.skill_id, input_sr.drafter_id)


@project_students_router.post("/{student_id}", status_code=status.HTTP_201_CREATED, response_class=Response, dependencies=[Depends(require_coach)])
async def add_student_to_project(student_id: int, input_sr: InputStudentRole, db: Session = Depends(get_session),
                                 project: Project = Depends(get_project)):
    """
    Add a student to a project.

    This is not a definitive decision, but represents a coach drafting the student.
    """
    logic_add_student_project(db, project, student_id, input_sr.skill_id, input_sr.drafter_id)
