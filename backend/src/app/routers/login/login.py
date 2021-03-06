import aiohttp
import sqlalchemy.exc
from fastapi import APIRouter, Form
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.exceptions.authentication import InvalidCredentialsException
from src.app.logic.security import authenticate_user_email, create_tokens, authenticate_user_github
from src.app.logic.users import get_user_editions
from src.app.routers.tags import Tags
from src.app.schemas.editions import Edition
from src.app.schemas.login import Token
from src.app.schemas.users import user_model_to_schema
from src.app.utils.dependencies import get_user_from_refresh_token, get_http_session
from src.database.database import get_session
from src.database.models import User

login_router = APIRouter(prefix="/login", tags=[Tags.LOGIN])


@login_router.post("/token/email", response_model=Token)
async def login_email(db: AsyncSession = Depends(get_session), form_data: OAuth2PasswordRequestForm = Depends()):
    """Called when logging in, generates an access token to use in other functions"""
    try:
        user = await authenticate_user_email(db, form_data.username, form_data.password)
    except sqlalchemy.exc.NoResultFound as not_found:
        # Don't use our own error handler here because this should
        # be a 401 instead of a 404
        raise InvalidCredentialsException() from not_found

    return await generate_token_response_for_user(db, user)


@login_router.post("/token/github")
async def login_github(http_session: aiohttp.ClientSession = Depends(get_http_session),
                       db: AsyncSession = Depends(get_session), code: str = Form(...)):
    """Called when logging in through GitHub, generates an access token"""
    try:
        user = await authenticate_user_github(http_session, db, code)
    except sqlalchemy.exc.NoResultFound as not_found:
        raise InvalidCredentialsException() from not_found

    return await generate_token_response_for_user(db, user)


@login_router.post("/refresh", response_model=Token)
async def refresh_access_token(db: AsyncSession = Depends(get_session),
                               user: User = Depends(get_user_from_refresh_token)):
    """
    Return a new access & refresh token using on the old refresh token

    Swagger note: This endpoint will not work on swagger because it uses the access token to try & refresh
    """
    return await generate_token_response_for_user(db, user)


async def generate_token_response_for_user(db: AsyncSession, user: User) -> Token:
    """
    Generate new tokens for a user and put them in the Token response schema.
    """
    access_token, refresh_token = create_tokens(user)

    user_data: dict = user_model_to_schema(user).__dict__
    editions = await get_user_editions(db, user)
    user_data["editions"] = list(map(Edition.from_orm, editions))

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        user=user_data
    )
