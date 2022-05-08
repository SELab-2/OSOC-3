from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

import src.app.logic.projects as logic_projects
import src.database.crud.projects_students as crud
from src.app.exceptions.projects import StudentInConflictException, FailedToAddProjectRoleException
from src.app.schemas.projects import ConflictStudentList
from src.database.models import Project, ProjectRole, Student, Skill


async def remove_student_project(db: AsyncSession, project: Project, student_id: int):
    """Remove a student from a project"""
    await crud.remove_student_project(db, project, student_id)


async def add_student_project(db: AsyncSession, project: Project, student_id: int, skill_id: int, drafter_id: int):
    """Add a student to a project"""
    # check this project-skill combination does not exist yet
    subquery = select(ProjectRole).where(ProjectRole.skill_id == skill_id).where(ProjectRole.project == project)\
        .subquery()
    count = (await db.execute(select(func.count()).select_from(subquery))).scalar_one()
    if count > 0:
        raise FailedToAddProjectRoleException
    # check that the student has the skill
    student = (await db.execute(select(Student).where(Student.student_id == student_id))).unique().scalar_one()
    skill = (await db.execute(select(Skill).where(Skill.skill_id == skill_id))).scalar_one()
    if skill not in student.skills:
        raise FailedToAddProjectRoleException
    # check that the student has not been confirmed in another project yet
    subquery_proj_definitive = select(ProjectRole).where(ProjectRole.student == student)\
        .where(ProjectRole.definitive.is_(True)).subquery()
    count_proj_definitive = (await db.execute(select(func.count()).select_from(subquery_proj_definitive))).scalar_one()
    if count_proj_definitive > 0:
        raise FailedToAddProjectRoleException
    # check that the project requires the skill
    project = (await db.execute(select(Project).where(Project.project_id == project.project_id))).unique().scalar_one()
    if skill not in project.skills:
        raise FailedToAddProjectRoleException

    await crud.add_student_project(db, project, student_id, skill_id, drafter_id)


async def change_project_role(db: AsyncSession, project: Project, student_id: int, skill_id: int, drafter_id: int):
    """Change the role of the student in the project"""
    # check this project-skill combination does not exist yet
    subquery = select(ProjectRole).where(ProjectRole.skill_id == skill_id).where(ProjectRole.project == project) \
        .subquery()
    count = (await db.execute(select(func.count()).select_from(subquery))).scalar_one()
    if count > 0:
        raise FailedToAddProjectRoleException
    # check that the student has the skill
    student = (await db.execute(select(Student).where(Student.student_id == student_id))).unique().scalar_one()
    skill = (await db.execute(select(Skill).where(Skill.skill_id == skill_id))).scalar_one()
    if skill not in student.skills:
        raise FailedToAddProjectRoleException
    # check that the student has not been confirmed in another project yet
    subquery_proj_definitive = select(ProjectRole).where(ProjectRole.student == student) \
        .where(ProjectRole.definitive.is_(True)).subquery()
    count_proj_definitive = (await db.execute(select(func.count()).select_from(subquery_proj_definitive))).scalar_one()
    if count_proj_definitive > 0:
        raise FailedToAddProjectRoleException
    # check that the project requires the skill
    project = (await db.execute(select(Project).where(Project.project_id == project.project_id))).unique().scalar_one()
    if skill not in project.skills:
        raise FailedToAddProjectRoleException

    await crud.change_project_role(db, project, student_id, skill_id, drafter_id)


async def confirm_project_role(db: AsyncSession, project: Project, student_id: int):
    """Definitively bind this student to the project"""
    # check if there are any conflicts concerning this student
    conflict_list: ConflictStudentList = await logic_projects.get_conflicts(db, project.edition)
    for conflict in conflict_list.conflict_students:
        if conflict.student.student_id == student_id:
            raise StudentInConflictException

    await crud.confirm_project_role(db, project, student_id)
