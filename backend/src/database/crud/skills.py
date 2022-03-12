from sqlalchemy.orm import Session
from src.database.models import Edition
from src.database.models import Skill
from src.app.schemas.skills import SkillBase
from typing import List


def get_skills(db: Session) -> List[Edition]:
    """Get a list of all the base skills that can be added to a student or project.

    Args:
        db (Session, optional): connection with the database. Defaults to Depends(get_session).

    Returns:
        List[Skill]: a list of all the skills of an edition.
    """
    return db.query(Skill).all()
     # return db.query(Skill).filter_by(edition_id = edition_id)


def create_skill(db: Session, skill: SkillBase) -> Skill:
    """Add a new skill into the database.

    Args:
        db (Session): connection with the database.
        skill (SkillBase): has all the fields needed to add a skill.

    Returns:
        Skill: returns the new skill.
    """
    new_skill: Skill = Skill()
    new_skill.name = skill.name
    new_skill.description = skill.description
    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)
    return new_skill


def delete_skill(db: Session, skill_id: int) -> bool:
    """Delete an existing skill.

    Args:
        db (Session): connection with the database.
        skill_id (int): the id of the skill
    """
    skill_to_delete = db.get(Skill, skill_id)
    if skill_to_delete is not None:
        db.delete(skill_to_delete)
        db.commit()
        return True
    else: return False