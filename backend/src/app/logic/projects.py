from sqlalchemy.orm import Session

from src.app.schemas.projects import ProjectList, Project, ConflictProjectList, ConflictProject
from src.database.crud.projects import db_get_all_projects, db_add_project, db_get_project, db_delete_project, \
    db_patch_project, db_get_conflict_students_for_project, db_get_all_conflict_projects
from src.database.models import Edition


def get_project_list(db: Session, edition: Edition) -> ProjectList:
    db_all_projects = db_get_all_projects(db, edition)
    return ProjectList(projects=db_all_projects)


def logic_create_project(db: Session, edition: Edition, name: str, number_of_students: int):
    db_add_project(db, edition, name, number_of_students)


def logic_get_project(db: Session, project_id: int) -> Project:
    project = db_get_project(db, project_id)
    return project


def logic_delete_project(db: Session, project_id: int):
    db_delete_project(db, project_id)


def logic_patch_project(db: Session, project_id: int, name: str, number_of_students: int):
    db_patch_project(db, project_id, name, number_of_students)


def logic_get_conflicts(db: Session, edition: Edition) -> ConflictProjectList:
    output = []
    projects = db_get_all_conflict_projects(db, edition)
    for project in projects:
        students = db_get_conflict_students_for_project(db, project)
        output.append(ConflictProject(project_id=project.project_id, name=project.name,
                                      number_of_students=project.number_of_students,
                                      edition_id=project.edition_id, conflicting_students=students))
    return ConflictProjectList(output)
