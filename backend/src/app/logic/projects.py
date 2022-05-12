from sqlalchemy.ext.asyncio import AsyncSession

import src.app.logic.partners as partners_logic
import src.database.crud.projects as crud
from src.app.schemas.projects import (
    ProjectList, ConflictStudentList, InputProject, InputProjectRole, QueryParamsProjects,
    ProjectRoleResponseList
)
from src.database.models import Edition, Project, ProjectRole, User


async def get_project_list(db: AsyncSession, edition: Edition, search_params: QueryParamsProjects,
                           user: User) -> ProjectList:
    """Returns a list of all projects from a certain edition"""
    proj_page = await crud.get_projects_for_edition_page(db, edition, search_params, user)

    return ProjectList(projects=proj_page)


async def create_project(db: AsyncSession, edition: Edition, input_project: InputProject) -> Project:
    """Create a new project"""
    try:
        # Fetch or create all partners
        partners = await partners_logic.get_or_create_partners_by_name(db, input_project.partners, commit=False)

        # Create the project
        project = await crud.create_project(db, edition, input_project, partners, commit=False)

        # Save the changes to the database
        await db.commit()

        return project
    except Exception as ex:
        # When an error occurs undo al database changes
        await db.rollback()
        raise ex


async def patch_project(db: AsyncSession, project: Project, input_project: InputProject) -> Project:
    """Make changes to a project"""
    try:
        # Fetch or create all partners
        partners = await partners_logic.get_or_create_partners_by_name(db, input_project.partners, commit=False)

        await crud.patch_project(db, project, input_project, partners, commit=False)

        # Save the changes to the database
        await db.commit()

        return project
    except Exception as ex:
        # When an error occurs undo al database changes
        await db.rollback()
        raise ex


async def delete_project(db: AsyncSession, project: Project):
    """Delete a project"""
    await crud.delete_project(db, project)


async def get_project_roles(db: AsyncSession, project: Project) -> ProjectRoleResponseList:
    """Get project roles for a project"""
    return ProjectRoleResponseList(project_roles=(await crud.get_project_roles_for_project(db, project)))


async def create_project_role(db: AsyncSession, project: Project, input_project_role: InputProjectRole) -> ProjectRole:
    """Create a project role"""
    return await crud.create_project_role(db, project, input_project_role)


async def patch_project_role(db: AsyncSession, project_role_id: int, input_project_role: InputProjectRole) \
        -> ProjectRole:
    """Update a project role"""
    return await crud.patch_project_role(db, project_role_id, input_project_role)


async def get_conflicts(db: AsyncSession, edition: Edition) -> ConflictStudentList:
    """Returns a list of all students together with the projects they are causing a conflict for"""
    return ConflictStudentList(conflict_students=(await crud.get_conflict_students(db, edition)))
