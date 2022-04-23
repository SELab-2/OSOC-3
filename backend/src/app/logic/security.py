import enum
from datetime import timedelta, datetime

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

import settings
from src.app.exceptions.authentication import InvalidCredentialsException
from src.database import models
from src.database.crud.users import get_user_by_email
from src.database.models import User

# Configuration

ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@enum.unique
class TokenType(enum.Enum):
    ACCESS = "access"
    REFRESH = "refresh"


def create_tokens(user: User) -> tuple[str, str]:
    """
    Create an access token and refresh token.

    Returns: (access_token, refresh_token)
    """
    return (
        _create_token({"type": TokenType.ACCESS.value, "sub": str(user.user_id)}, settings.ACCESS_TOKEN_EXPIRE_M),
        _create_token({"type": TokenType.REFRESH.value, "sub": str(user.user_id)}, settings.REFRESH_TOKEN_EXPIRE_M)
    )


def _create_token(data: dict, expires_delta: int) -> str:
    """Encode the user data with an expiry timestamp to create the token"""
    # The 'exp' key here is extremely important. if this key changes expiry will not be checked.
    data["exp"] = datetime.utcnow() + timedelta(minutes=expires_delta)
    return jwt.encode(data, settings.SECRET_KEY, algorithm=ALGORITHM)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify that a password matches a hash found in the database"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def authenticate_user(db: Session, email: str, password: str) -> models.User:
    """Match an email/password combination to a User model"""
    user = get_user_by_email(db, email)

    if user.email_auth.pw_hash is None or not verify_password(password, user.email_auth.pw_hash):
        raise InvalidCredentialsException()

    return user
