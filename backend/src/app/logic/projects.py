from sqlalchemy.orm import Session

import src.app.logic.partners as partners_logic
import src.database.crud.projects as crud
from src.app.schemas.projects import (
    ProjectList, ConflictStudentList, InputProject, ConflictStudent, InputProjectRole, QueryParamsProjects
)
from src.database.models import Edition, Project, ProjectRole, User


def get_project_list(db: Session, edition: Edition, search_params: QueryParamsProjects, user: User) -> ProjectList:
    """Returns a list of all projects from a certain edition"""
    return ProjectList(projects=crud.get_projects_for_edition_page(db, edition, search_params, user))


def create_project(db: Session, edition: Edition, input_project: InputProject) -> Project:
    """Create a new project"""
    try:
        # Fetch or create all partners
        partners = partners_logic.get_or_create_partners_by_name(db, input_project.partners, commit=False)

        # Create the project
        project = crud.create_project(db, edition, input_project, partners, commit=False)

        # Save the changes to the database
        db.commit()

        return project
    except Exception as ex:
        # When an error occurs undo al database changes
        db.rollback()
        raise ex


def patch_project(db: Session, project: Project, input_project: InputProject) -> Project:
    """Make changes to a project"""
    try:
        # Fetch or create all partners
        partners = partners_logic.get_or_create_partners_by_name(db, input_project.partners, commit=False)

        crud.patch_project(db, project, input_project, partners, commit=False)

        # Save the changes to the database
        db.commit()

        return project
    except Exception as ex:
        # When an error occurs undo al database changes
        db.rollback()
        raise ex


def delete_project(db: Session, project: Project):
    """Delete a project"""
    crud.delete_project(db, project)


def get_project_roles(db: Session, project: Project) -> list[ProjectRole]:
    return crud.get_project_roles_for_project(db, project)


def create_project_role(db: Session, project: Project, input_project_role: InputProjectRole) -> ProjectRole:
    return crud.create_project_role(db, project, input_project_role)


def patch_project_role(db: Session, project_role_id: int, input_project_role: InputProjectRole) -> ProjectRole:
    return crud.patch_project_role(db, project_role_id, input_project_role)


def get_conflicts(db: Session, edition: Edition) -> ConflictStudentList:
    """Returns a list of all students together with the projects they are causing a conflict for"""
    print(crud.get_conflict_students(db, edition))
    return ConflictStudentList(conflict_students=crud.get_conflict_students(db, edition))
