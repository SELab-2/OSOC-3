from sqlalchemy.orm import Session

from src.app.schemas.projects import ProjectList, Project, ConflictStudentList, InputProject
from src.database.crud.projects import db_get_all_projects, db_add_project, db_delete_project, \
    db_patch_project, db_get_conflict_students
from src.database.models import Edition


def logic_get_project_list(db: Session, edition: Edition) -> ProjectList:
    """Returns a list of all projects from a certain edition"""
    db_all_projects = db_get_all_projects(db, edition)
    return ProjectList(projects=db_all_projects)


def logic_create_project(db: Session, edition: Edition, input_project: InputProject) -> Project:
    """Create a new project"""
    project = db_add_project(db, edition, input_project)
    return Project(project_id=project.project_id, name=project.name, number_of_students=project.number_of_students,
                   edition_id=project.edition_id, coaches=project.coaches, skills=project.skills,
                   partners=project.partners, project_roles=project.project_roles)


def logic_delete_project(db: Session, project_id: int):
    """Delete a project"""
    db_delete_project(db, project_id)


def logic_patch_project(db: Session, project: Project, input_project: InputProject):
    """Make changes to a project"""
    db_patch_project(db, project, input_project)


def logic_get_conflicts(db: Session, edition: Edition) -> ConflictStudentList:
    """Returns a list of all students together with the projects they are causing a conflict for"""
    conflicts = db_get_conflict_students(db, edition)
    return ConflictStudentList(conflict_students=conflicts)
