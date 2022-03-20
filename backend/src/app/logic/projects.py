from sqlalchemy.orm import Session

from src.app.schemas.projects import ProjectList, Project, ConflictStudentList, ProjectId
from src.database.crud.projects import db_get_all_projects, db_add_project, db_delete_project, \
    db_patch_project, db_get_conflict_students
from src.database.models import Edition


def logic_get_project_list(db: Session, edition: Edition) -> ProjectList:
    """Returns a list of all projects from a certain edition"""
    db_all_projects = db_get_all_projects(db, edition)
    return ProjectList(projects=db_all_projects)


def logic_create_project(db: Session, edition: Edition, name: str, number_of_students: int, skills: list[int],
                         partners: list[str], coaches: list[int]) -> ProjectId:
    """Create a new project"""
    return db_add_project(db, edition, name, number_of_students, skills, partners, coaches)


def logic_delete_project(db: Session, project_id: int):
    """Delete a project"""
    db_delete_project(db, project_id)


def logic_patch_project(db: Session, project: Project, name: str, number_of_students: int, skills: [int],
                        partners: list[str], coaches: list[int]):
    """Make changes to a project"""
    db_patch_project(db, project, name, number_of_students, skills, partners, coaches)


def logic_get_conflicts(db: Session, edition: Edition) -> ConflictStudentList:
    """Returns a list of all students together with the projects they are causing a conflict for"""
    conflicts = db_get_conflict_students(db, edition)
    return ConflictStudentList(conflict_students=conflicts)
