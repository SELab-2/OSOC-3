import sqlalchemy.exc
from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.app.exceptions.authentication import InvalidCredentialsException
from src.app.logic.security import authenticate_user, create_tokens
from src.app.logic.users import get_user_editions
from src.app.routers.tags import Tags
from src.app.schemas.login import Token, UserData
from src.app.schemas.users import user_model_to_schema
from src.app.utils.dependencies import get_current_active_user, get_user_from_refresh_token
from src.database.database import get_session
from src.database.models import User

login_router = APIRouter(prefix="/login", tags=[Tags.LOGIN])


@login_router.post("/token", response_model=Token)
async def login_for_access_token(db: Session = Depends(get_session),
                                 form_data: OAuth2PasswordRequestForm = Depends()):
    """Called when logging in, generates an access token to use in other functions"""
    try:
        user = authenticate_user(db, form_data.username, form_data.password)
    except sqlalchemy.exc.NoResultFound as not_found:
        # Don't use our own error handler here because this should
        # be a 401 instead of a 404
        raise InvalidCredentialsException() from not_found

    access_token, refresh_token = create_tokens(user)

    user_data: dict = user_model_to_schema(user).__dict__
    user_data["editions"] = get_user_editions(db, user)

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        user=UserData(**user_data)
    )


@login_router.post("/refresh", response_model=Token)
async def refresh_access_token(db: Session = Depends(get_session), user: User = Depends(get_user_from_refresh_token)):
    """Return a new access & refresh token using on the old refresh token

    Swagger note: This endpoint will not work on swagger because it uses the access token to try & refresh"""
    access_token, refresh_token = create_tokens(user)

    user_data: dict = user_model_to_schema(user).__dict__
    user_data["editions"] = get_user_editions(db, user)

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        user=UserData(**user_data)
    )
