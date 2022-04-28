from sqlalchemy.orm import Session

from src.database.models import AuthEmail, CoachRequest, User, Edition


def create_user(db: Session, name: str, commit: bool = True) -> User:
    """Create a user"""
    new_user: User = User(name=name)
    db.add(new_user)

    if commit:
        db.commit()

    return new_user


def create_coach_request(db: Session, user: User, edition: Edition, commit: bool = True) -> CoachRequest:
    """Create a coach request"""
    coach_request: CoachRequest = CoachRequest(user=user, edition=edition)
    db.add(coach_request)

    if commit:
        db.commit()

    return coach_request


def create_auth_email(db: Session, user: User, pw_hash: str, email: str, commit: bool = True) -> AuthEmail:
    """Create a authentication for email"""
    auth_email: AuthEmail = AuthEmail(user=user, pw_hash=pw_hash, email=email)
    db.add(auth_email)

    if commit:
        db.commit()

    return auth_email
