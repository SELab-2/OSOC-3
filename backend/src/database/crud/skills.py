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


async def get_skill_by_id(db: AsyncSession, skill_id: int) -> Skill:
    """Get a skill for a id"""
    return (await db.execute(select(Skill).where(Skill.skill_id == skill_id))).scalar_one()


async def create_skill(db: AsyncSession, skill: SkillBase) -> Skill:
    """Add a new skill into the database."""
    new_skill: Skill = Skill(name=skill.name)
    db.add(new_skill)
    await db.commit()
    await db.refresh(new_skill)
    return new_skill


async def delete_skill(db: AsyncSession, skill_id: int):
    """Delete an existing skill."""
    # query a skill to return 404 if it doesn't exist
    (await (db.execute(select(Skill).where(Skill.skill_id == skill_id)))).scalars().one()
    await db.execute(delete(Skill).where(Skill.skill_id == skill_id))
    await db.commit()


async def create_skill_if_not_present(db: AsyncSession, name: str) -> bool:
    """Create a skill if it doesn't exist"""
    existing = (await db.execute(select(Skill).where(Skill.name == name))).one_or_none()
    if existing:
        return False

    # Create the skill
    await create_skill(db, SkillBase(name=name))
    return True
