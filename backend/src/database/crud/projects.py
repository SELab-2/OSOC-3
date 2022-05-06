from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

from src.app.schemas.projects import InputProject, QueryParamsProjects
from src.database.crud.util import paginate
from src.database.models import Project, Edition, Student, ProjectRole, Skill, User, Partner


def _get_projects_for_edition_query(edition: Edition) -> Select:
    return select(Project).where(Project.edition == edition).order_by(Project.project_id)


async def get_projects_for_edition(db: AsyncSession, edition: Edition) -> list[Project]:
    """Returns a list of all projects from a certain edition from the database"""
    result = await db.execute(_get_projects_for_edition_query(edition))
    return result.scalars().all()


async def get_projects_for_edition_page(db: AsyncSession, edition: Edition,
                                        search_params: QueryParamsProjects, user: User) -> list[Project]:
    """Returns a paginated list of all projects from a certain edition from the database"""
    query = _get_projects_for_edition_query(edition).where(
        Project.name.contains(search_params.name))
    if search_params.coach:
        query = query.where(Project.project_id.in_([user_project.project_id for user_project in user.projects]))
    result = await db.execute(paginate(query, search_params.page))
    projects: list[Project] = result.scalars().all()

    return projects


async def _get_skill_by_id(db_skill: AsyncSession, skill_id: int) -> Skill:
    query_skill = select(Skill).where(Skill.skill_id == skill_id)
    result_skill = await db_skill.execute(query_skill)
    return result_skill.scalars().one()


async def _get_coach_by_id(db_coach: AsyncSession, coach_id: int) -> User:
    query_coach = select(User).where(User.user_id == coach_id)
    result_coach = await db_coach.execute(query_coach)
    return result_coach.scalars().one()


async def add_project(db: AsyncSession, edition: Edition, input_project: InputProject) -> Project:
    """
    Add a project to the database
    If there are partner names that are not already in the database, add them
    """

    skills_obj = [await _get_skill_by_id(db, skill)
                  for skill in input_project.skills]
    coaches_obj = [await _get_coach_by_id(db, coach)
                   for coach in input_project.coaches]
    partners_obj = []
    for partner in input_project.partners:
        try:
            query = select(Partner).where(Partner.name == partner)
            result = await db.execute(query)
            partners_obj.append(result.scalars().one())
        except NoResultFound:
            partner_obj = Partner(name=partner)
            db.add(partner_obj)
            partners_obj.append(partner_obj)
    project = Project(name=input_project.name, number_of_students=input_project.number_of_students,
                      edition_id=edition.edition_id, skills=skills_obj, coaches=coaches_obj, partners=partners_obj)

    db.add(project)
    await db.commit()
    return project


async def get_project(db: AsyncSession, project_id: int) -> Project:
    """Query a specific project from the database through its ID"""
    query = select(Project).where(Project.project_id == project_id)
    result = await db.execute(query)
    return result.scalars().one()


async def delete_project(db: AsyncSession, project_id: int):
    """Delete a specific project from the database"""
    query = select(ProjectRole).where(ProjectRole.project_id == project_id)
    result = await db.execute(query)
    proj_roles = result.scalars().all()
    for proj_role in proj_roles:
        await db.delete(proj_role)

    project = await get_project(db, project_id)
    await db.delete(project)
    await db.commit()


async def patch_project(db: AsyncSession, project_id: int, input_project: InputProject):
    """
    Change some fields of a Project in the database
    If there are partner names that are not already in the database, add them
    """
    project = get_project(db, project_id)

    skills_obj = [await _get_skill_by_id(db, skill)
                  for skill in input_project.skills]
    coaches_obj = [await _get_coach_by_id(db, coach)
                   for coach in input_project.coaches]
    partners_obj = []
    for partner in input_project.partners:
        try:
            query = select(Partner).where(Partner.name == partner)
            result = await db.execute(query)
            partners_obj.append(result.scalars().one())
        except NoResultFound:
            partner_obj = Partner(name=partner)
            db.add(partner_obj)
            partners_obj.append(partner_obj)

    project.name = input_project.name
    project.number_of_students = input_project.number_of_students
    project.skills = skills_obj
    project.coaches = coaches_obj
    project.partners = partners_obj
    await db.commit()


async def get_conflict_students(db: AsyncSession, edition: Edition) -> list[tuple[Student, list[Project]]]:
    """
    Query all students that are causing conflicts for a certain edition
    Return a ConflictStudent for each student that causes a conflict
    This class contains a student together with all projects they are causing a conflict for
    """
    query = select(Student).where(Student.edition == edition)
    result = await db.execute(query)
    students = result.scalars().all()

    conflict_students = []
    projs = []
    for student in students:
        if len(student.project_roles) > 1:
            result_proj_ids = await db.execute(select(ProjectRole.project_id)
                                               .where(ProjectRole.student_id == student.student_id))
            proj_ids = result_proj_ids.scalars().all()
            for proj_id in proj_ids:
                proj_id = proj_id[0]
                result_proj = await db.execute(select(Project).where(Project.project_id == proj_id))
                proj = result_proj.scalars().one()
                projs.append(proj)
            conflict_student = (student, projs)
            conflict_students.append(conflict_student)
    return conflict_students
