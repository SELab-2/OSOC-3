from sqlalchemy.orm import Session, Query

from src.app.schemas.projects import InputArgumentation
from src.database.models import ProjectRole, User, Student, ProjectRoleSuggestion


def _get_pr_suggestion_for_pr_by_student_query(db: Session, project_role: ProjectRole, student: Student) -> Query:
    return db.query(ProjectRoleSuggestion).where(
        ProjectRoleSuggestion.project_role == project_role and
        ProjectRoleSuggestion.student == student
    )


def get_pr_suggestion_for_pr_by_student(
        db: Session,
        project_role: ProjectRole,
        student: Student) -> ProjectRoleSuggestion:
    """Get the project role suggestion for a student"""
    return _get_pr_suggestion_for_pr_by_student_query(db, project_role, student).one()


def get_optional_pr_suggestion_for_pr_by_student(
        db: Session,
        project_role: ProjectRole,
        student: Student) -> ProjectRoleSuggestion | None:
    """Get the project role suggestion for a student, but don't raise an error when none is found"""
    return _get_pr_suggestion_for_pr_by_student_query(db, project_role, student).one_or_none()


def create_pr_suggestion(
        db: Session,
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
    db.commit()
    return pr_suggestion


def update_pr_suggestion(
        db: Session,
        pr_suggestion: ProjectRoleSuggestion,
        drafter: User,
        argumentation: InputArgumentation) -> ProjectRoleSuggestion:
    """Update a project role suggestion"""
    pr_suggestion.argumentation = argumentation.argumentation
    pr_suggestion.drafter = drafter
    db.commit()
    return pr_suggestion


def remove_project_role_suggestion(db: Session, project_role: ProjectRole, student: Student):
    """Remove a student from a project in the database"""
    project_role_suggestion = db.query(ProjectRoleSuggestion).where(
        ProjectRoleSuggestion.student == student and
        ProjectRoleSuggestion.project_role == project_role
    ).one()
    db.delete(project_role_suggestion)
    db.commit()
