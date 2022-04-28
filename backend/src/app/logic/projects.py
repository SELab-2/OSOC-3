from sqlalchemy.orm import Session

import src.database.crud.projects as crud
from src.app.schemas.projects import (
    ProjectList, ConflictStudentList, InputProject, ConflictStudent, QueryParamsProjects
)
from src.database.models import Edition, Project, User


def get_project_list(db: Session, edition: Edition, search_params: QueryParamsProjects, user: User) -> ProjectList:
    """Returns a list of all projects from a certain edition"""
    return ProjectList(projects=crud.get_projects_for_edition_page(db, edition, search_params, user))


def create_project(db: Session, edition: Edition, input_project: InputProject) -> Project:
    """Create a new project"""
    return crud.add_project(db, edition, input_project)


def delete_project(db: Session, project_id: int):
    """Delete a project"""
    crud.delete_project(db, project_id)


def patch_project(db: Session, project_id: int, input_project: InputProject):
    """Make changes to a project"""
    crud.patch_project(db, project_id, input_project)


def get_conflicts(db: Session, edition: Edition) -> ConflictStudentList:
    """Returns a list of all students together with the projects they are causing a conflict for"""
    conflicts = crud.get_conflict_students(db, edition)
    conflicts_model = []
    for student, projects in conflicts:
        conflicts_model.append(ConflictStudent(student=student, projects=projects))

    return ConflictStudentList(conflict_students=conflicts_model)
