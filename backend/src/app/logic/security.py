from datetime import timedelta, datetime

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

import settings
from src.app.exceptions.authentication import InvalidCredentialsException
from src.database import models

# Configuration
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Encode the user data with an expire timestamp to create the token"""
    to_encode = data.copy()

    if expires_delta is not None:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_HOURS)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify that a password matches a hash found in the database"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


# TO DO remove this when the users crud has been implemented
def get_user_by_email(db: Session, email: str) -> models.User:
    """Find a user by their email address"""
    auth_email = db.query(models.AuthEmail).where(models.AuthEmail.email == email).one()
    return db.query(models.User).where(models.User.user_id == auth_email.user_id).one()


# TO DO remove this when the users crud has been implemented
def get_user_by_id(db: Session, user_id: int) -> models.User:
    """Find a user by their id"""
    return db.query(models.User).where(models.User.user_id == user_id).one()


def authenticate_user(db: Session, email: str, password: str) -> models.User:
    """Match an email/password combination to a User model"""
    user = get_user_by_email(db, email)

    if not verify_password(password, user.email_auth.pw_hash):
        raise InvalidCredentialsException()

    return user
