
from sqlalchemy.orm import Session

from src.app.exceptions.register import FailedToAddNewUserException
from src.database.models import AuthEmail, CoachRequest, User, Edition


def create_user(db: Session, name: str) -> User:
    """Create a user"""
    new_user: User = User(name=name)
    db.add(new_user)
    db.commit()
    return new_user


def create_coach_request(db: Session, user: User, edition: Edition) -> CoachRequest:
    """Create a coach request"""
    coach_request: CoachRequest = CoachRequest(user=user, edition=edition)
    db.add(coach_request)
    db.commit()
    return coach_request


def create_auth_email(db: Session, user: User, pw_hash: str, email: str) -> AuthEmail:
    """Create a authentication for email"""
    auth_email: AuthEmail = AuthEmail(user=user, pw_hash=pw_hash, email=email)
    db.add(auth_email)
    db.commit()
    return auth_email


def create_user_with_auth(db: Session, name: str, pw_hash: str, email: str) -> User:
    new_user: User = User(name=name)
    db.add(new_user)
    auth_email: AuthEmail = AuthEmail(user=new_user, pw_hash=pw_hash, email=email)
    db.add(auth_email)
    try:
        db.commit()
    except Exception as exception:
        raise FailedToAddNewUserException from exception

    return new_user
