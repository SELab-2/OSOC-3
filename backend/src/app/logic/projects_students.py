from sqlalchemy.ext.asyncio import AsyncSession

import src.database.crud.projects_students as crud
from src.app.exceptions.crud import DuplicateInsertException
from src.app.schemas.projects import (
    InputArgumentation, ReturnProjectRoleSuggestion)
from src.database.models import ProjectRole, Student, User, ProjectRoleSuggestion


async def remove_project_role_suggestion(db: AsyncSession, project_role: ProjectRole, student: Student):
    """Remove a student from a project"""
    await crud.remove_project_role_suggestion(db, project_role, student)


async def add_student_project(
        db: AsyncSession,
        project_role: ProjectRole,
        student: Student,
        drafter: User,
        argumentation: InputArgumentation) -> ReturnProjectRoleSuggestion:
    """Add a student to a project"""
    pr_suggestion = await crud.get_optional_pr_suggestion_for_pr_by_student(db, project_role, student)
    if pr_suggestion is None:
        project_role_suggestion: ProjectRoleSuggestion = \
            await crud.create_pr_suggestion(db, project_role, student, drafter, argumentation)
        return ReturnProjectRoleSuggestion(project_role_suggestion=project_role_suggestion)
    raise DuplicateInsertException()


async def change_project_role_suggestion(
        db: AsyncSession,
        project_role: ProjectRole,
        student: Student,
        updater: User,
        argumentation: InputArgumentation):
    """Change the role of the student in the project"""
    pr_suggestion = await crud.get_pr_suggestion_for_pr_by_student(db, project_role, student)
    await crud.update_pr_suggestion(db, pr_suggestion, updater, argumentation)
