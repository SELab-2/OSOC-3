from sqlalchemy.orm import Session

from src.database.models import AuthEmail, CoachRequest, User, Edition

import hashlib

def create_user(db: Session, name: str, email: str) -> User:
    """Create a user"""
    new_user: User = User(name=name, email=email)
    db.add(new_user)
    db.commit()
    return new_user

def create_coach_request(db: Session, user: User, edition: Edition) -> CoachRequest:
    """Create a coach request"""
    coach_request: CoachRequest = CoachRequest(user=user, edition=edition)
    db.add(coach_request)
    db.commit()
    return coach_request

def create_auth_email(db: Session, user: User, pw: str) -> AuthEmail:
    """Create a authentication for email"""
    pw_hash = hashlib.sha512(pw.encode("UTF-8")).hexdigest()
    auth_email : AuthEmail = AuthEmail(user=user, pw_hash = pw_hash)
    db.add(auth_email)
    db.commit()
    return auth_email