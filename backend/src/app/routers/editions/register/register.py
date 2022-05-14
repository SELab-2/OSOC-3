from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.app.logic.register import create_request
from src.app.routers.tags import Tags
from src.app.schemas.register import NewUser
from src.app.utils.dependencies import get_latest_edition
from src.database.database import get_session
from src.database.models import Edition

registration_router = APIRouter(prefix="/register", tags=[Tags.REGISTRATION])


@registration_router.post("/email", status_code=status.HTTP_201_CREATED)
async def register_email(user: NewUser, db: AsyncSession = Depends(get_session),
                         edition: Edition = Depends(get_latest_edition)):
    """
    Register a new account using the email/password format.
    """
    await create_request(db, user, edition)
