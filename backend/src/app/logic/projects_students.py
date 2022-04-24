from sqlalchemy.orm import Session

import src.database.crud.projects_students as crud
from src.app.exceptions.editions import DuplicateInsertException
from src.app.schemas.projects import InputArgumentation
from src.database.models import ProjectRole, Student, User, ProjectRoleSuggestion


def remove_project_role_suggestion(db: Session, project_role: ProjectRole, student: Student):
    """Remove a student from a project"""
    crud.remove_project_role_suggestion(db, project_role, student)


def add_student_project(
        db: Session,
        project_role: ProjectRole,
        student: Student,
        drafter: User,
        argumentation: InputArgumentation) -> ProjectRoleSuggestion:
    """Add a student to a project"""
    pr_suggestion = crud.get_optional_pr_suggestion_for_pr_by_student(db, project_role, student)
    if pr_suggestion is None:
        return crud.create_pr_suggestion(db, project_role, student, drafter, argumentation)
    else:
        raise DuplicateInsertException()


def change_project_role_suggestion(
        db: Session,
        project_role: ProjectRole,
        student: Student,
        updater: User,
        argumentation: InputArgumentation):
    """Change the role of the student in the project"""
    pr_suggestion = crud.get_pr_suggestion_for_pr_by_student(db, project_role, student)
    return crud.update_pr_suggestion(db, pr_suggestion, updater, argumentation)
