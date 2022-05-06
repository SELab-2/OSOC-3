from sqlalchemy.ext.asyncio import AsyncSession

import src.database.crud.projects as crud
from src.app.schemas.projects import (
    ProjectList, ConflictStudentList, InputProject, ConflictStudent, QueryParamsProjects
)
from src.database.models import Edition, Project, User

async def get_project_list(db: AsyncSession, edition: Edition, search_params: QueryParamsProjects,
                           user: User) -> ProjectList:
    """Returns a list of all projects from a certain edition"""
    proj_page = await crud.get_projects_for_edition_page(db, edition, search_params, user)

    return ProjectList(projects=proj_page)


async def create_project(db: AsyncSession, edition: Edition, input_project: InputProject) -> Project:
    """Create a new project"""
    return await crud.add_project(db, edition, input_project)


async def delete_project(db: AsyncSession, project_id: int):
    """Delete a project"""
    await crud.delete_project(db, project_id)


async def patch_project(db: AsyncSession, project_id: int, input_project: InputProject):
    """Make changes to a project"""
    await crud.patch_project(db, project_id, input_project)


async def get_conflicts(db: AsyncSession, edition: Edition) -> ConflictStudentList:
    """Returns a list of all students together with the projects they are causing a conflict for"""
    conflicts = await crud.get_conflict_students(db, edition)
    conflicts_model = []
    for student, projects in conflicts:
        conflicts_model.append(ConflictStudent(student=student, projects=projects))

    return ConflictStudentList(conflict_students=conflicts_model)
