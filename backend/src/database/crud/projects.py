from sqlalchemy.orm import Session

from src.database.models import Project, Edition, Student, ProjectRole


def db_get_all_projects(db: Session, edition: Edition) -> list[Project]:
    return db.query(Project).where(Project.edition == edition).all()


def db_add_project(db: Session, edition: Edition, name: str, number_of_students: int):
    project = Project(name=name, number_of_students=number_of_students, edition_id=edition.edition_id)
    db.add(project)
    db.commit()


def db_get_project(db: Session, project_id: int) -> Project:
    return db.query(Project).where(Project.project_id == project_id).one()


def db_delete_project(db: Session, project_id: int):
    project = db_get_project(db, project_id)
    db.delete(project)
    db.commit()


def db_patch_project(db: Session, project_id: int, name: str, number_of_students: int):
    project = db_get_project(db, project_id)
    project.name = name
    project.number_of_students = number_of_students
    db.commit()


def db_get_all_conflict_projects(db: Session, edition: Edition) -> list[Project]:
    return db.query(Project).where(len(Project.project_roles) > Project.number_of_students)\
        .where(Project.edition == edition).all()


def db_get_conflict_students_for_project(db: Session, project: Project) -> list[Student]:
    students = db.query(ProjectRole.student).where(ProjectRole.project_id == project.project_id)\
        .where(len(ProjectRole.student.project_roles) > 1).all()

    return students
