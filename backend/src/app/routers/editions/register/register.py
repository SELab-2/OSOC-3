from fastapi import APIRouter

from src.app.routers.tags import Tags

registration_router = APIRouter(prefix="/register", tags=[Tags.REGISTRATION])


@registration_router.post("/email")
async def register_email(edition_id: int):
    """
    Register a new account using the email/password format.
    """
