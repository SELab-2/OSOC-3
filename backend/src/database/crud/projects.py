from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

import src.database.crud.skills as skills_crud
from src.app.schemas.projects import InputProject, InputProjectRole, QueryParamsProjects
from src.database.crud.users import get_user_by_id
from src.database.crud.util import paginate
from src.database.models import Project, Edition, Student, ProjectRole, Partner, User


def _get_projects_for_edition_query(edition: Edition) -> Select:
    return select(Project).where(Project.edition == edition)


async def get_projects_for_edition(db: AsyncSession, edition: Edition) -> list[Project]:
    """Returns a list of all projects from a certain edition from the database"""
    result = await db.execute(_get_projects_for_edition_query(edition).order_by(Project.name))
    return result.unique().scalars().all()


async def get_projects_for_edition_page(
        db: AsyncSession,
        edition: Edition,
        search_params: QueryParamsProjects,
        user: User) -> list[Project]:
    """Returns a paginated list of all projects from a certain edition from the database"""
    query = _get_projects_for_edition_query(edition).where(
        Project.name.contains(search_params.name))
    if search_params.coach:
        query = query.where(Project.project_id.in_([user_project.project_id for user_project in user.projects]))
    result = await db.execute(paginate(query.order_by(Project.name), search_params.page))
    return result.unique().scalars().all()


async def create_project(
        db: AsyncSession,
        edition: Edition,
        input_project: InputProject,
        partners: list[Partner],
        commit: bool = True) -> Project:
    """
    Add a project to the database
    If there are partner names that are not already in the database, add them
    """
    coaches = [await get_user_by_id(db, coach) for coach in input_project.coaches]

    project = Project(
        name=input_project.name,
        edition_id=edition.edition_id,
        coaches=coaches,
        partners=partners
    )

    db.add(project)

    if commit:
        await db.commit()

    return project


async def get_project(db: AsyncSession, project_id: int) -> Project:
    """Query a specific project from the database through its ID"""
    query = select(Project).where(Project.project_id == project_id)
    result = await db.execute(query)
    project = result.unique().scalars().one()
    # refresh to see updated relations
    await db.refresh(project)
    return project


async def delete_project(db: AsyncSession, project: Project):
    """Delete a specific project from the database"""
    await db.delete(project)
    await db.commit()


async def patch_project(
        db: AsyncSession,
        project: Project,
        input_project: InputProject,
        partners: list[Partner],
        commit: bool = True):
    """
    Change some fields of a Project in the database
    If there are partner names that are not already in the database, add them
    """
    coaches = [await get_user_by_id(db, coach) for coach in input_project.coaches]

    project.name = input_project.name
    project.coaches = coaches
    project.partners = partners

    if commit:
        await db.commit()


async def get_project_role(db: AsyncSession, project_role_id: int) -> ProjectRole:
    """Get a project role by id"""
    return (await db.execute(select(ProjectRole).where(ProjectRole.project_role_id == project_role_id))).unique()\
        .scalar_one()


async def get_project_roles_for_project(db: AsyncSession, project: Project) -> list[ProjectRole]:
    """Get the project roles associated with a project"""
    return (await db.execute(select(ProjectRole).where(ProjectRole.project == project))).unique().scalars().all()


async def create_project_role(db: AsyncSession, project: Project, input_project_role: InputProjectRole) -> ProjectRole:
    """Create a project role for a project"""
    skill = await skills_crud.get_skill_by_id(db, input_project_role.skill_id)

    project_role = ProjectRole(
        project=project,
        skill=skill,
        description=input_project_role.description,
        slots=input_project_role.slots
    )

    db.add(project_role)
    await db.commit()
    # query project_role to create association tables
    (await db.execute(select(ProjectRole).where(ProjectRole.project_role_id == project_role.project_role_id)))
    return project_role


async def patch_project_role(
        db: AsyncSession,
        project_role_id: int,
        input_project_role: InputProjectRole) -> ProjectRole:
    """Create a project role for a project"""
    skill = await skills_crud.get_skill_by_id(db, input_project_role.skill_id)
    project_role = await get_project_role(db, project_role_id)

    project_role.skill = skill
    project_role.description = input_project_role.description
    project_role.slots = input_project_role.slots

    await db.commit()
    return project_role


async def get_conflict_students(db: AsyncSession, edition: Edition) -> list[Student]:
    """
    Return an overview of the students that are assigned to multiple projects
    """
    return [
        s for s in (await db.execute(select(Student).where(Student.edition == edition))).unique().scalars().all()
        if len(s.pr_suggestions) > 1
    ]
