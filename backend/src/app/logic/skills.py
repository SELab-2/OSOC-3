from sqlalchemy.orm import Session

from src.app.schemas.skills import SkillBase, SkillList
import src.database.crud.skills as crud_skills
from src.database.models import Skill


def get_skills(db: Session) -> SkillList:
    """Get a list of all the base skills that can be added to a student or project.

    Args:
        db (Session): connection with the database.

    Returns:
        SkillList: an object with a list of all the skills.
    """
    return SkillList(skills=crud_skills.get_skills(db))


def create_skill(db: Session, skill: SkillBase) -> Skill:
    """Add a new skill into the database.

    Args:
        skill (SkillBase): has all the fields needed to add a skill.
        db (Session): connection with the database.

    Returns:
        Skill: returns the new skill.
    """
    return crud_skills.create_skill(db, skill)


def delete_skill(db: Session, skill_id: int):
    """Delete an existing skill.

    Args:
        skill_id (int): the id of the skill.
        db (Session): connection with the database.
    """
    crud_skills.delete_skill(db, skill_id)
