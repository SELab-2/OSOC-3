from sqlalchemy.ext.asyncio import AsyncSession

import src.database.crud.skills as crud_skills
from src.app.schemas.skills import SkillBase, SkillList
from src.database.models import Skill


async def get_skills(db: AsyncSession) -> SkillList:
    """Get a list of all the base skills that can be added to a student or project.

    Args:
        db (Session): connection with the database.

    Returns:
        SkillList: an object with a list of all the skills.
    """
    skills = await crud_skills.get_skills(db)
    return SkillList(skills=skills)


async def create_skill(db: AsyncSession, skill: SkillBase) -> Skill:
    """Add a new skill into the database.

    Args:
        skill (SkillBase): has all the fields needed to add a skill.
        db (Session): connection with the database.

    Returns:
        Skill: returns the new skill.
    """
    return await crud_skills.create_skill(db, skill)


async def delete_skill(db: AsyncSession, skill_id: int):
    """Delete an existing skill.

    Args:
        skill_id (int): the id of the skill.
        db (Session): connection with the database.
    """
    await crud_skills.delete_skill(db, skill_id)
