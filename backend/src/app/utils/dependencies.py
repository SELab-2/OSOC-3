import sqlalchemy.exc
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, ExpiredSignatureError, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

import settings
import src.database.crud.projects as crud_projects
from src.app.exceptions.authentication import (
    ExpiredCredentialsException, InvalidCredentialsException,
    MissingPermissionsException, WrongTokenTypeException)
from src.app.exceptions.editions import ReadOnlyEditionException
from src.app.logic.security import ALGORITHM, TokenType
from src.database.crud.editions import get_edition_by_name, latest_edition
from src.database.crud.invites import get_invite_link_by_uuid
from src.database.crud.students import get_student_by_id
from src.database.crud.suggestions import get_suggestion_by_id
from src.database.crud.users import get_user_by_id
from src.database.database import get_session
from src.database.models import Edition, InviteLink, Student, Suggestion, User, Project


async def get_edition(edition_name: str, database: AsyncSession = Depends(get_session)) -> Edition:
    """Get an edition from the database, given the name in the path"""
    return await get_edition_by_name(database, edition_name)


async def get_student(student_id: int, database: AsyncSession = Depends(get_session)) -> Student:
    """Get the student from the database, given the id in the path"""
    return await get_student_by_id(database, student_id)


async def get_suggestion(suggestion_id: int, database: AsyncSession = Depends(get_session)) -> Suggestion:
    """Get the suggestion from the database, given the id in the path"""
    return await get_suggestion_by_id(database, suggestion_id)


async def get_latest_edition(edition: Edition = Depends(get_edition), database: AsyncSession = Depends(get_session)) -> Edition:
    """Checks if the given edition is the latest one (others are read-only) and returns it if it is"""
    latest = await latest_edition(database)
    if edition != latest:
        raise ReadOnlyEditionException
    return latest


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")


async def _get_user_from_token(token_type: TokenType, db: AsyncSession, token: str) -> User:
    """Check which user is making a request by decoding its token, and verifying the token type"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int | None = payload.get("sub")
        type_in_token: int | None = payload.get("type")

        if user_id is None or type_in_token is None:
            raise InvalidCredentialsException()

        if type_in_token != token_type.value:
            raise WrongTokenTypeException()

        try:
            user = await get_user_by_id(db, int(user_id))
        except sqlalchemy.exc.NoResultFound as not_found:
            raise InvalidCredentialsException() from not_found

        return user
    except ExpiredSignatureError as expired_signature:
        raise ExpiredCredentialsException() from expired_signature
    except JWTError as jwt_err:
        raise InvalidCredentialsException() from jwt_err


async def get_user_from_access_token(db: AsyncSession = Depends(get_session),
                                     token: str = Depends(oauth2_scheme)) -> User:
    """Check which user is making a request by decoding its access token
    This function is used as a dependency for other functions
    """
    return await _get_user_from_token(TokenType.ACCESS, db, token)


async def get_user_from_refresh_token(db: AsyncSession = Depends(get_session), token: str = Depends(oauth2_scheme)) -> User:
    """Check which user is making a request by decoding its refresh token
    This function is used as a dependency for other functions
    """
    return await _get_user_from_token(TokenType.REFRESH, db, token)


async def require_auth(user: User = Depends(get_user_from_access_token)) -> User:
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


async def require_admin(user: User = Depends(get_user_from_access_token)) -> User:
    """Dependency to create an admin-only route"""
    if not user.admin:
        raise MissingPermissionsException()

    return user


async def require_coach(edition: Edition = Depends(get_edition),
                        user: User = Depends(get_user_from_access_token)) -> User:
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


async def get_invite_link(invite_uuid: str, db: AsyncSession = Depends(get_session)) -> InviteLink:
    """Get an invite link from the database, given the id in the path"""
    return await get_invite_link_by_uuid(db, invite_uuid)


async def get_project(project_id: int, db: AsyncSession = Depends(get_session)) -> Project:
    """Get a project from het database, given the id in the path"""
    return await crud_projects.get_project(db, project_id)
