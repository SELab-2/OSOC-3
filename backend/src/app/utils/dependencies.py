import sqlalchemy.exc
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, ExpiredSignatureError, JWTError
from sqlalchemy.orm import Session

import settings
from src.app.exceptions.authentication import ExpiredCredentialsException, InvalidCredentialsException, \
    MissingPermissionsException
from src.app.logic.security import ALGORITHM, get_user_by_id
from src.database.crud.editions import get_edition_by_name
from src.database.crud.invites import get_invite_link_by_uuid
from src.database.crud.projects import db_get_project
from src.database.database import get_session
from src.database.models import Edition, InviteLink, User, Project


def get_edition(edition_name: str, database: Session = Depends(get_session)) -> Edition:
    """Get an edition from the database, given the name in the path"""
    return get_edition_by_name(database, edition_name)


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


async def require_auth(user: User = Depends(get_current_active_user)) -> User:
    """Dependency to check if a user is at least a coach
    This dependency should be used to check for resources that aren't linked to
    editions

    The function checks if the user is either an admin, or a coach with at least
    one UserRole (meaning they have been accepted for at least one edition)
    """
    # Admins can see everything
    if user.admin:
        return user

    # Coach is not in any editions (yet)
    if len(user.editions) == 0:
        raise MissingPermissionsException()

    return user


async def require_admin(user: User = Depends(get_current_active_user)) -> User:
    """Dependency to create an admin-only route"""
    if not user.admin:
        raise MissingPermissionsException()

    return user


async def require_coach(edition: Edition = Depends(get_edition), user: User = Depends(get_current_active_user)) -> User:
    """Dependency to check if a user can see a given resource
    This comes down to checking if a coach is linked to an edition or not
    """
    # Admins can see everything in any edition
    if user.admin:
        return user

    # Coach is not part of this edition
    if edition not in user.editions:
        raise MissingPermissionsException()

    return user


def get_invite_link(invite_uuid: str, db: Session = Depends(get_session)) -> InviteLink:
    """Get an invite link from the database, given the id in the path"""
    return get_invite_link_by_uuid(db, invite_uuid)


def get_project(project_id: int, db: Session = Depends(get_session)) -> Project:
    """Get a project from het database, given the id in the path"""
    return db_get_project(db, project_id)
