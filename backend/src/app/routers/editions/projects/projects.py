from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import Response

from src.app.logic.projects import logic_get_project_list, logic_create_project, logic_delete_project, \
    logic_patch_project, logic_get_conflicts
from src.app.routers.tags import Tags
from src.app.schemas.projects import ProjectList, Project, ConflictProjectList
from src.app.utils.dependencies import get_edition, get_project
from src.database.database import get_session
from src.database.models import Edition
from .students import project_students_router

projects_router = APIRouter(prefix="/projects", tags=[Tags.PROJECTS])
projects_router.include_router(project_students_router, prefix="/{project_id}")


@projects_router.get("/", response_model=ProjectList)
async def get_projects(db: Session = Depends(get_session), edition: Edition = Depends(get_edition)):
    """
    Get a list of all projects.
    """
    return logic_get_project_list(db, edition)


@projects_router.post("/", status_code=status.HTTP_201_CREATED, response_class=Response)
async def create_project(name: str, number_of_students: int, skills: list[int], partners: list[str], coaches: list[int],
                         db: Session = Depends(get_session), edition: Edition = Depends(get_edition)):
    """
    Create a new project.users
    """
    logic_create_project(db, edition, name, number_of_students, skills, partners, coaches)


@projects_router.get("/conflicts", response_model=ConflictProjectList)
async def get_conflicts(db: Session = Depends(get_session), edition: Edition = Depends(get_edition)):
    """
    Get a list of all projects with conflicts, and the users that
    are causing those conflicts.
    """
    # return all projects which have more students than listed, and all students who are in more than one project
    return logic_get_conflicts(db, edition)


@projects_router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_project(project_id: int, db: Session = Depends(get_session)):
    """
    Delete a specific project.
    """
    return logic_delete_project(db, project_id)


@projects_router.get("/{project_id}", status_code=status.HTTP_200_OK, response_model=Project)
async def get_project(project: Project = Depends(get_project)):
    """
    Get information about a specific project.
    """
    return project


@projects_router.patch("/{project_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def patch_project(name: str, number_of_students: int, skills: list[int], partners: list[str],
                        coaches: list[int], project: Project = Depends(get_project),
                        db: Session = Depends(get_session)):
    """
    Update a project, changing some fields.
    """
    logic_patch_project(db, project, name, number_of_students, skills, partners, coaches)
