from sqlalchemy.orm import Session

from src.app.schemas.skills import SkillBase
from src.database.models import Skill


def get_skills(db: Session) -> list[Skill]:
    """Get a list of all the base skills that can be added to a student or project.

    Args:
        db (Session): connection with the database.

    Returns:
        SkillList: an object with a list of all the skills.
    """
    return db.query(Skill).all()


def get_skills_by_ids(db: Session, skill_ids) -> list[Skill]:
    """Get all skills from list of skill ids"""
    return db.query(Skill).where(Skill.skill_id.in_(skill_ids)).all()


def create_skill(db: Session, skill: SkillBase) -> Skill:
    """Add a new skill into the database.

    Args:
        db (Session): connection with the database.
        skill (SkillBase): has all the fields needed to add a skill.

    Returns:
        Skill: returns the new skill.
    """
    new_skill: Skill = Skill(name=skill.name, description=skill.description)
    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)
    return new_skill


def delete_skill(db: Session, skill_id: int):
    """Delete an existing skill.

    Args:
        db (Session): connection with the database.
        skill_id (int): the id of the skill
    """
    db.delete(db.query(Skill).where(Skill.skill_id == skill_id).one())
    db.commit()
