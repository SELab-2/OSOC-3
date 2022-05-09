from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.schemas.skills import SkillBase
from src.database.models import Skill


async def get_skills(db: AsyncSession) -> list[Skill]:
    """Get a list of all the base skills that can be added to a student or project.

    Args:
        db (Session): connection with the database.

    Returns:
        SkillList: an object with a list of all the skills.
    """
    return (await db.execute(select(Skill))).scalars().all()


async def get_skills_by_ids(db: AsyncSession, skill_ids) -> list[Skill]:
    """Get all skills from list of skill ids"""
    return (await db.execute(select(Skill).where(Skill.skill_id.in_(skill_ids)))).scalars().all()


async def create_skill(db: AsyncSession, skill: SkillBase) -> Skill:
    """Add a new skill into the database.

    Args:
        db (Session): connection with the database.
        skill (SkillBase): has all the fields needed to add a skill.

    Returns:
        Skill: returns the new skill.
    """
    new_skill: Skill = Skill(name=skill.name, description=skill.description)
    db.add(new_skill)
    await db.commit()
    await db.refresh(new_skill)
    return new_skill


async def delete_skill(db: AsyncSession, skill_id: int):
    """Delete an existing skill.

    Args:
        db (Session): connection with the database.
        skill_id (int): the id of the skill
    """
    skill_to_delete = delete(Skill).where(Skill.skill_id == skill_id)
    await db.execute(skill_to_delete)
    await db.commit()
