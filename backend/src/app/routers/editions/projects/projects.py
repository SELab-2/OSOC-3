from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import Response

from src.app.logic.projects import logic_get_project_list, logic_create_project, logic_delete_project, \
    logic_patch_project, logic_get_conflicts
from src.app.routers.tags import Tags
from src.app.schemas.projects import ProjectList, Project, InputProject, \
    ConflictStudentList
from src.app.utils.dependencies import get_edition, get_project
from src.database.database import get_session
from src.database.models import Edition, Project as ProjectDB
from .students import project_students_router

projects_router = APIRouter(prefix="/projects", tags=[Tags.PROJECTS])
projects_router.include_router(project_students_router, prefix="/{project_id}")


@projects_router.get("/", response_model=ProjectList)
async def get_projects(db: Session = Depends(get_session), edition: Edition = Depends(get_edition)):
    """
    Get a list of all projects.
    """
    return logic_get_project_list(db, edition)


@projects_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Project)
async def create_project(input_project: InputProject,
                         db: Session = Depends(get_session), edition: Edition = Depends(get_edition)):
    """
    Create a new project
    """
    return logic_create_project(db, edition,
                                input_project.name,
                                input_project.number_of_students,
                                input_project.skills, input_project.partners, input_project.coaches)


@projects_router.get("/conflicts", response_model=ConflictStudentList)
async def get_conflicts(db: Session = Depends(get_session), edition: Edition = Depends(get_edition)):
    """
    Get a list of all projects with conflicts, and the users that
    are causing those conflicts.
    """
    return logic_get_conflicts(db, edition)


@projects_router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_project(project_id: int, db: Session = Depends(get_session)):
    """
    Delete a specific project.
    """
    return logic_delete_project(db, project_id)


@projects_router.get("/{project_id}", status_code=status.HTTP_200_OK, response_model=Project)
async def get_project(project: ProjectDB = Depends(get_project)):
    """
    Get information about a specific project.
    """
    project_model = Project(project_id=project.project_id, name=project.name,
                            number_of_students=project.number_of_students,
                            edition_name=project.edition.name, coaches=project.coaches, skills=project.skills,
                            partners=project.partners, project_roles=project.project_roles)
    return project_model


@projects_router.patch("/{project_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def patch_project(project_id: int, input_project: InputProject, db: Session = Depends(get_session)):
    """
    Update a project, changing some fields.
    """
    logic_patch_project(db, project_id, input_project.name,
                        input_project.number_of_students,
                        input_project.skills, input_project.partners, input_project.coaches)
