from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from src.app.logic import skills as logic_skills
from src.app.routers.tags import Tags
from src.app.schemas.skills import SkillBase, Skill, SkillList
from src.app.utils.dependencies import require_auth
from src.database.database import get_session

skills_router = APIRouter(prefix="/skills", tags=[Tags.SKILLS])


@skills_router.get("", response_model=SkillList, tags=[Tags.SKILLS], dependencies=[Depends(require_auth)])
async def get_skills(db: Session = Depends(get_session)):
    """Get a list of all the base skills that can be added to a student or project.

    Args:
        db (Session, optional): connection with the database. Defaults to Depends(get_session).

    Returns:
        SkillList: an object with a list of all the skills.
    """
    return logic_skills.get_skills(db)


@skills_router.post("", status_code=status.HTTP_201_CREATED, response_model=Skill, tags=[Tags.SKILLS],
                    dependencies=[Depends(require_auth)])
async def create_skill(skill: SkillBase, db: Session = Depends(get_session)):
    """Add a new skill into the database.

    Args:
        skill (SkillBase): has all the fields needed to add a skill.
        db (Session, optional): connection with the database. Defaults to Depends(get_session).

    Returns:
        Skill: returns the new skill.
    """
    return logic_skills.create_skill(db, skill)


@skills_router.delete("/{skill_id}", status_code=status.HTTP_204_NO_CONTENT, tags=[Tags.SKILLS],
                      dependencies=[Depends(require_auth)])
async def delete_skill(skill_id: int, db: Session = Depends(get_session)):
    """Delete an existing skill.

    Args:
        skill_id (int): the id of the skill.
        db (Session, optional): connection with the database. Defaults to Depends(get_session).
    """
    logic_skills.delete_skill(db, skill_id)
