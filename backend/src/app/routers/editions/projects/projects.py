from fastapi import APIRouter

from src.app.routers.tags import Tags
from .students import project_students_router

projects_router = APIRouter(prefix="/projects", tags=[Tags.PROJECTS])
projects_router.include_router(project_students_router, prefix="/{project_id}")


@projects_router.get("/")
async def get_projects(edition_id: int):
    """
    Get a list of all projects.
    """


@projects_router.post("/")
async def create_project(edition_id: int):
    """
    Create a new project.
    """


@projects_router.get("/conflicts")
async def get_conflicts(edition_id: int):
    """
    Get a list of all projects with conflicts, and the users that
    are causing those conflicts.
    """


@projects_router.delete("/{project_id}")
async def delete_project(edition_id: int, project_id: int):
    """
    Delete a specific project.
    """


@projects_router.get("/{project_id}")
async def get_project(edition_id: int, project_id: int):
    """
    Get information about a specific project.
    """


@projects_router.patch("/{project_id}")
async def patch_project(edition_id: int, project_id: int):
    """
    Update a project, changing some fields.
    """
