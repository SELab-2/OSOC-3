from sqlalchemy.orm import Session

from src.app.schemas.register import NewUser
from src.database.models import Edition
from src.database.crud.register import create_user, create_auth_email, create_coach_request

def create_request(db: Session, new_user: NewUser, edition: Edition) -> None:
    """Create a coach request. But when something failed, the changed aren't commited"""
    try:
        user = create_user(db, new_user.name, new_user.email)
        create_auth_email(db, user, new_user.pw)
        create_coach_request(db, user, edition)
    except:
        db.rollback()
    finally:
        db.commit()