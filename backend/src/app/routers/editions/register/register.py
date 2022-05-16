from aiohttp import ClientSession
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.app.logic.oauth.github import get_github_access_token, get_github_profile
from src.app.logic.register import create_request_email, create_request_github
from src.app.routers.tags import Tags
from src.app.schemas.register import EmailRegister, GitHubRegister
from src.app.utils.dependencies import get_latest_edition, get_http_session
from src.database.database import get_session
from src.database.models import Edition

registration_router = APIRouter(prefix="/register", tags=[Tags.REGISTRATION])


@registration_router.post("/email", status_code=status.HTTP_201_CREATED)
async def register_email(register_data: EmailRegister, db: AsyncSession = Depends(get_session),
                         edition: Edition = Depends(get_latest_edition)):
    """
    Register a new account using the email/password format.
    """
    await create_request_email(db, register_data, edition)


@registration_router.post("/github", status_code=status.HTTP_201_CREATED)
async def register_github(register_data: GitHubRegister, db: AsyncSession = Depends(get_session),
                          http_session: ClientSession = Depends(get_http_session),
                          edition: Edition = Depends(get_latest_edition)):
    """Register a new account using GitHub OAuth."""
    access_token_data = await get_github_access_token(http_session, register_data.code)
    user_email = await get_github_profile(http_session, access_token_data.access_token)
    await create_request_github(db, user_email, register_data.uuid, edition)
