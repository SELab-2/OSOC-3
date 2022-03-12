from sqlalchemy.orm import Session
from backend.src.database.models import Edition
from src.database.models import Skill
from src.app.schemas.skills import SkillBase
from typing import List, Optional


def get_skills(db: Session, edition_id: int) -> List[Edition]:
    """Get a list of all the base skills that can be added to a student or project.

    Args:
        edition_id (int): the id of the edition you want to get the skills of.
        db (Session, optional): connection with the database. Defaults to Depends(get_session).

    Returns:
        List[Skill]: a list of all the skills of an edition.
    """
    return db.query(Skill).all()
     # return db.query(Skill).filter_by(edition_id = edition_id)
