from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Project, ProjectRole, Skill, User, Student


async def remove_student_project(db: AsyncSession, project: Project, student_id: int):
    """Remove a student from a project in the database"""
    query = select(ProjectRole).where(ProjectRole.student_id == student_id).where(ProjectRole.project == project)
    result = await db.execute(query)
    proj_role = result.scalars().one()
    await db.delete(proj_role)
    await db.commit()


async def add_student_project(db: AsyncSession, project: Project, student_id: int, skill_id: int, drafter_id: int):
    """Add a student to a project in the database"""

    # check if all parameters exist in the database
    (await db.execute(select(Skill).where(Skill.skill_id == skill_id))).scalars().one()
    (await db.execute(select(User).where(User.user_id == drafter_id))).unique().one()
    (await db.execute(select(Student).where(Student.student_id == student_id))).unique().one()

    proj_role = ProjectRole(student_id=student_id, project_id=project.project_id, skill_id=skill_id,
                            drafter_id=drafter_id)
    db.add(proj_role)
    await db.commit()


async def change_project_role(db: AsyncSession, project: Project, student_id: int, skill_id: int, drafter_id: int):
    """Change the role of a student in a project and update the drafter"""

    # check if all parameters exist in the database
    (await db.execute(select(Skill).where(Skill.skill_id == skill_id))).scalars().one()
    (await db.execute(select(User).where(User.user_id == drafter_id))).unique().one()
    (await db.execute(select(Student).where(Student.student_id == student_id))).unique().one()

    proj_role = (await db.execute(select(ProjectRole).where(
        ProjectRole.student_id == student_id).where(ProjectRole.project == project))).scalar_one()
    proj_role.drafter_id = drafter_id
    proj_role.skill_id = skill_id
    await db.commit()


async def confirm_project_role(db: AsyncSession, project: Project, student_id: int):
    """Confirm a project role"""
    query = select(ProjectRole).where(ProjectRole.student_id == student_id) \
        .where(ProjectRole.project == project)
    result = await db.execute(query)
    proj_role = result.scalars().one()

    proj_role.definitive = True
    await db.commit()
