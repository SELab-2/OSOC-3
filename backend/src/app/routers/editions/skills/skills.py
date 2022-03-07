from fastapi import APIRouter

from fastapi import Depends
from src.database.database import get_session
from src.database.models import Skill
from src.database.schemas import SkillBase
from sqlalchemy.orm import Session

from typing import List

from src.app.routers.tags import Tags

# Should be added in a schema file



skills_router = APIRouter(prefix="/skills", tags=[Tags.SKILLS])


@skills_router.get("/")
async def get_skills(edition_id: int, db: Session = Depends(get_session)) -> List[Skill]:
    """Get a list of all the base skills that can be added to a student or project.

    Args:
        edition_id (int): the id of the edition you want to get the skills of.
        db (Session, optional): connection with the database. Defaults to Depends(get_session).

    Returns:
        List[Skill]: a list of all the skills of an edition.
    """
    return db.query(Skill).all()
    # return db.query(Skill).filter_by(edition_id = edition_id)



@skills_router.post("/")
async def create_skill(edition_id: int, skill: SkillBase, db: Session = Depends(get_session)) -> Skill:
    """Add a new skill into the database.

    Args:
        edition_id (int): the id of the edition you want to add a skill to.
        skill (SkillBase): has all the fields needed to add a skill.
        db (Session, optional): connection with the database. Defaults to Depends(get_session).

    Returns:
        Skill: returns the new skill.
    """
    new_skill: Skill = Skill()
    new_skill.name = skill.name
    new_skill.description = skill.name
    # new_skill.edition_id = edition_id
    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)
    return new_skill
