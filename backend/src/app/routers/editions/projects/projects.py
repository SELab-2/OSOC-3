from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import Response

import src.app.logic.projects as logic
from src.app.routers.tags import Tags
from src.app.schemas.projects import (
    InputProjectRole,
    ProjectRole as ProjectRoleSchema, ProjectRoleResponseList)
from src.app.schemas.projects import (
    ProjectList, Project, InputProject, ConflictStudentList, QueryParamsProjects
)
from src.app.utils.dependencies import get_edition, get_project, require_admin, require_coach, get_editable_edition
from src.app.utils.websockets import live
from src.database.database import get_session
from src.database.models import Edition, Project as ProjectModel, User
from .students import project_students_router

projects_router = APIRouter(prefix="/projects", tags=[Tags.PROJECTS])
projects_router.include_router(project_students_router, prefix="/{project_id}/roles/{project_role_id}")


@projects_router.get("", response_model=ProjectList)
async def get_projects(
        db: AsyncSession = Depends(get_session),
        edition: Edition = Depends(get_edition),
        search_params: QueryParamsProjects = Depends(QueryParamsProjects),
        user: User = Depends(require_coach)):
    """Get a list of all projects."""
    return await logic.get_project_list(db, edition, search_params, user)


@projects_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=Project,
    dependencies=[Depends(require_admin)]
)
async def create_project(
        input_project: InputProject,
        db: AsyncSession = Depends(get_session),
        edition: Edition = Depends(get_editable_edition)):
    """Create a new project"""
    return await logic.create_project(db, edition,
                                      input_project)


@projects_router.get("/conflicts", response_model=ConflictStudentList, dependencies=[Depends(require_coach)])
async def get_conflicts(db: AsyncSession = Depends(get_session), edition: Edition = Depends(get_edition)):
    """
    Get a list of all projects with conflicts, and the users that
    are causing those conflicts.
    """
    return await logic.get_conflicts(db, edition)


@projects_router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT, response_class=Response,
    dependencies=[Depends(require_admin), Depends(live)]
)
async def delete_project(project: ProjectModel = Depends(get_project), db: AsyncSession = Depends(get_session)):
    """Delete a specific project."""
    return await logic.delete_project(db, project)


@projects_router.get(
    "/{project_id}",
    status_code=status.HTTP_200_OK,
    response_model=Project,
    dependencies=[Depends(require_coach)]
)
async def get_project_route(project: ProjectModel = Depends(get_project)):
    """Get information about a specific project."""
    return project


@projects_router.patch(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT, response_class=Response,
    dependencies=[Depends(require_admin), Depends(get_editable_edition), Depends(live)]
)
async def patch_project(
        input_project: InputProject,
        project: ProjectModel = Depends(get_project),
        db: AsyncSession = Depends(get_session)):
    """
    Update a project, changing some fields.
    """
    await logic.patch_project(db, project, input_project)


@projects_router.get(
    "/{project_id}/roles",
    response_model=ProjectRoleResponseList,
    dependencies=[Depends(require_coach), Depends(get_edition)]
)
async def get_project_roles(project: ProjectModel = Depends(get_project), db: AsyncSession = Depends(get_session)):
    """List all project roles for a project"""
    return await logic.get_project_roles(db, project)


@projects_router.post(
    "/{project_id}/roles",
    response_model=ProjectRoleSchema,
    dependencies=[Depends(require_admin), Depends(get_editable_edition), Depends(live)],
    status_code=status.HTTP_201_CREATED
)
async def post_project_role(
        input_project_role: InputProjectRole,
        project: ProjectModel = Depends(get_project),
        db: AsyncSession = Depends(get_session)):
    """Create a new project role"""
    return await logic.create_project_role(db, project, input_project_role)


@projects_router.patch(
    "/{project_id}/roles/{project_role_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProjectRoleSchema,
    dependencies=[Depends(require_admin), Depends(get_editable_edition), Depends(get_project), Depends(live)]
)
async def patch_project_role(
        input_project_role: InputProjectRole,
        project_role_id: int,
        db: AsyncSession = Depends(get_session)):
    """Create a new project role"""
    return await logic.patch_project_role(db, project_role_id, input_project_role)


@projects_router.delete(
    "/{project_id}/roles/{project_role_id}",
    status_code=status.HTTP_204_NO_CONTENT, response_class=Response,
    dependencies=[Depends(require_admin), Depends(get_project), Depends(live)]
)
async def delete_project_role(
        project_role_id: int,
        db: AsyncSession = Depends(get_session)):
    """Delete a project role"""
    await logic.delete_project_role(db, project_role_id)
