from sqlalchemy.orm import Session

from src.database.models import AuthEmail, CoachRequest, User

import hashlib

def create_user(db: Session, name: str, email: str) -> User:
    new_user: User = User(name=name, email=email)
    db.add(new_user)
    db.commit()
    return new_user

def create_coach_request(db: Session, user: User) -> CoachRequest:
    coach_request: CoachRequest = CoachRequest(user=user)
    db.add(coach_request)
    db.commit()
    return coach_request

def create_auth_email(db: Session, user: User, pw: str) -> AuthEmail:
    pw_hash = hashlib.sha512(pw.encode("UTF-8")).hexdigest()
    auth_email : AuthEmail = AuthEmail(user=user, pw_hash = pw_hash)
    db.add(auth_email)
    db.commit()
    return auth_email