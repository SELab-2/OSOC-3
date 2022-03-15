import sqlalchemy.exc
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, ExpiredSignatureError, JWTError
from sqlalchemy.orm import Session

import settings
from src.app.exceptions.authentication import ExpiredCredentialsException, InvalidCredentialsException, UnauthorizedException
from src.app.logic.security import ALGORITHM, get_user_by_id
from src.database.crud.editions import get_edition_by_id
from src.database.database import get_session
from src.database.models import Edition, User


# TODO: Might be nice to use a more descriptive year number here than primary id.
def get_edition(edition_id: int, db: Session = Depends(get_session)) -> Edition:
    """Get an edition from the database, given the id in the path"""
    return get_edition_by_id(db, edition_id)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/token")


async def get_current_active_user(db: Session = Depends(get_session), token: str = Depends(oauth2_scheme)) -> User:
    """Check which user is making a request by decoding its token
    This function is used as a dependency for other functions
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int | None = payload.get("sub")

        if user_id is None:
            raise InvalidCredentialsException()

        try:
            user = get_user_by_id(db, int(user_id))
        except sqlalchemy.exc.NoResultFound as not_found:
            raise InvalidCredentialsException() from not_found

        return user
    except ExpiredSignatureError as expired_signature:
        raise ExpiredCredentialsException() from expired_signature
    except JWTError as jwt_err:
        raise InvalidCredentialsException() from jwt_err


# Alias that is easier to read in the dependency list when
# the return value isn't required
# Require the user to be authorized, coach or admin doesn't matter
require_authorization = get_current_active_user
require_auth = get_current_active_user


async def require_admin(user: User = Depends(get_current_active_user)) -> User:
    """Dependency to create an admin-only route"""
    if not user.admin:
        raise UnauthorizedException()

    return user
