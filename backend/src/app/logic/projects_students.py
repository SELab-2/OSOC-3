from sqlalchemy.orm import Session

from src.database.crud.projects_students import db_remove_student_project, db_add_student_project, \
    db_change_project_role
from src.database.models import Project


def logic_remove_student_project(db: Session, project: Project, student_id: int):
    """Remove a student from a project"""
    db_remove_student_project(db, project, student_id)


def logic_add_student_project(db: Session, project: Project, student_id: int, skill_id: int, drafter_id: int):
    """Add a student to a project"""
    db_add_student_project(db, project, student_id, skill_id, drafter_id)


def logic_change_project_role(db: Session, project: Project, student_id: int, skill_id: int, drafter_id: int):
    """Change the role of the student in the project"""
    db_change_project_role(db, project, student_id, skill_id, drafter_id)
