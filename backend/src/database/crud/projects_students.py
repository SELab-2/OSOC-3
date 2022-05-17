from sqlalchemy import select
from sqlalchemy.sql import Select
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.schemas.projects import InputArgumentation
from src.database.models import ProjectRoleSuggestion

from src.database.models import ProjectRole, User, Student


def _get_pr_suggestion_for_pr_by_student_query(project_role: ProjectRole, student: Student) -> Select:
    return select(ProjectRoleSuggestion).where(
        ProjectRoleSuggestion.project_role == project_role).where(
        ProjectRoleSuggestion.student == student
    )


async def get_pr_suggestion_for_pr_by_student(
        db: AsyncSession,
        project_role: ProjectRole,
        student: Student) -> ProjectRoleSuggestion:
    """Get the project role suggestion for a student"""
    return (await db.execute(_get_pr_suggestion_for_pr_by_student_query(project_role, student))).scalar_one()


async def get_optional_pr_suggestion_for_pr_by_student(
        db: AsyncSession,
        project_role: ProjectRole,
        student: Student) -> ProjectRoleSuggestion | None:
    """Get the project role suggestion for a student, but don't raise an error when none is found"""
    return (await db.execute(_get_pr_suggestion_for_pr_by_student_query(project_role, student))).scalar_one_or_none()


async def create_pr_suggestion(
        db: AsyncSession,
        project_role: ProjectRole,
        student: Student,
        drafter: User,
        argumentation: InputArgumentation) -> ProjectRoleSuggestion:
    """Create a project role suggestion"""
    pr_suggestion = ProjectRoleSuggestion(
        project_role=project_role,
        student=student,
        drafter=drafter,
        argumentation=argumentation.argumentation
    )
    db.add(pr_suggestion)
    await db.commit()
    return pr_suggestion


async def update_pr_suggestion(
        db: AsyncSession,
        pr_suggestion: ProjectRoleSuggestion,
        drafter: User,
        argumentation: InputArgumentation) -> ProjectRoleSuggestion:
    """Update a project role suggestion"""
    pr_suggestion.argumentation = argumentation.argumentation
    pr_suggestion.drafter = drafter
    await db.commit()
    return pr_suggestion


async def remove_project_role_suggestion(db: AsyncSession, project_role: ProjectRole, student: Student):
    """Remove a student from a project in the database"""
    project_role_suggestion = (await db.execute(select(ProjectRoleSuggestion).where(
        ProjectRoleSuggestion.student == student).where(
        ProjectRoleSuggestion.project_role == project_role
    ))).scalar_one()
    await db.delete(project_role_suggestion)
    await db.commit()
    await db.refresh(project_role)
