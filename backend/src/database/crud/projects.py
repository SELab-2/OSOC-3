from sqlalchemy.orm import Session, Query

import src.database.crud.skills as skills_crud
from src.app.schemas.projects import InputProject, InputProjectRole, QueryParamsProjects
from src.database.crud.users import get_user_by_id
from src.database.crud.util import paginate
from src.database.models import Project, Edition, Student, ProjectRole, Partner, User


def _get_projects_for_edition_query(db: Session, edition: Edition) -> Query:
    return db.query(Project).where(Project.edition == edition).order_by(Project.project_id)


def get_projects_for_edition(db: Session, edition: Edition) -> list[Project]:
    """Returns a list of all projects from a certain edition from the database"""
    return _get_projects_for_edition_query(db, edition).all()


def get_projects_for_edition_page(
        db: Session,
        edition: Edition,
        search_params: QueryParamsProjects,
        user: User) -> list[Project]:
    """Returns a paginated list of all projects from a certain edition from the database"""
    query = _get_projects_for_edition_query(db, edition).where(
        Project.name.contains(search_params.name))
    if search_params.coach:
        query = query.where(Project.project_id.in_([user_project.project_id for user_project in user.projects]))
    projects: list[Project] = paginate(query, search_params.page).all()

    return projects


def create_project(
        db: Session,
        edition: Edition,
        input_project: InputProject,
        partners: list[Partner],
        commit: bool = True) -> Project:
    """
    Add a project to the database
    If there are partner names that are not already in the database, add them
    """
    coaches = [get_user_by_id(db, coach) for coach in input_project.coaches]

    project = Project(
        name=input_project.name,
        edition_id=edition.edition_id,
        coaches=coaches,
        partners=partners
    )

    db.add(project)

    if commit:
        db.commit()

    return project


def get_project(db: Session, project_id: int) -> Project:
    """Query a specific project from the database through its ID"""
    return db.query(Project).where(Project.project_id == project_id).one()


def delete_project(db: Session, project: Project):
    """Delete a specific project from the database"""
    db.delete(project)
    db.commit()


def patch_project(
        db: Session,
        project: Project,
        input_project: InputProject,
        partners: list[Partner],
        commit: bool = True):
    """
    Change some fields of a Project in the database
    If there are partner names that are not already in the database, add them
    """

    coaches = [get_user_by_id(db, coach) for coach in input_project.coaches]

    project.name = input_project.name
    project.coaches = coaches
    project.partners = partners

    if commit:
        db.commit()


def get_project_role(db: Session, project_role_id: int) -> ProjectRole:
    """Get a project role by id"""
    return db.query(ProjectRole).where(ProjectRole.project_role_id == project_role_id).one()


def get_project_roles_for_project(db: Session, project: Project) -> list[ProjectRole]:
    """Get the project roles associated with a project"""
    return db.query(ProjectRole).where(ProjectRole.project == project).all()


def create_project_role(db: Session, project: Project, input_project_role: InputProjectRole) -> ProjectRole:
    """Create a project role for a project"""
    skill = skills_crud.get_skill_by_id(db, input_project_role.skill_id)

    project_role = ProjectRole(
        project=project,
        skill=skill,
        description=input_project_role.description,
        slots=input_project_role.slots
    )

    db.add(project_role)
    db.commit()
    return project_role


def patch_project_role(
        db: Session,
        project_role_id: int,
        input_project_role: InputProjectRole) -> ProjectRole:
    """Create a project role for a project"""
    skill = skills_crud.get_skill_by_id(db, input_project_role.skill_id)
    project_role = get_project_role(db, project_role_id)

    project_role.skill = skill
    project_role.description = input_project_role.description
    project_role.slots = input_project_role.slots

    db.commit()
    return project_role


def get_conflict_students(db: Session, edition: Edition) -> list[Student]:
    """
    Return an overview of the students that are assigned to multiple projects
    """
    return [
        s for s in db.query(Student).where(Student.edition == edition).all()
        if len(s.pr_suggestions) > 1
    ]
