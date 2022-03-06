from fastapi import APIRouter

from src.app.routers.tags import Tags

skills_router = APIRouter(prefix="/skills", tags=[Tags.SKILLS])


@skills_router.get("/")
async def get_skills(edition_id: int):
    """
    Get a list of all the base skills that can be added to a student or project.
    """


@skills_router.post("/")
async def create_skill(edition_id: int):
    """
    Add a new skill into the database.
    """
