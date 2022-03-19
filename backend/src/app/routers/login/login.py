from datetime import timedelta

import sqlalchemy.exc
from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.app.exceptions.authentication import InvalidCredentialsException
from src.app.logic.security import authenticate_user, ACCESS_TOKEN_EXPIRE_HOURS, create_access_token
from src.app.routers.tags import Tags
from src.app.schemas.login import Token
from src.database.database import get_session

login_router = APIRouter(prefix="/login", tags=[Tags.LOGIN])


@login_router.post("/token", response_model=Token)
async def login_for_access_token(db: Session = Depends(get_session),
                                 form_data: OAuth2PasswordRequestForm = Depends()) -> dict[str, str]:
    """Called when logging in, generates an access token to use in other functions"""
    try:
        user = authenticate_user(db, form_data.username, form_data.password)
    except sqlalchemy.exc.NoResultFound as not_found:
        # Don't use our own error handler here because this should
        # be a 401 instead of a 404
        raise InvalidCredentialsException() from not_found
    
    access_token_expires = timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    access_token = create_access_token(
        data={"sub": str(user.user_id)}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
