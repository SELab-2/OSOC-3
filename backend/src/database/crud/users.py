from sqlalchemy import select

from src.database.models import User, UserRole
from sqlalchemy.orm import Session, aliased


def get_users_from_edition(db: Session, edition_id: int) -> list[User]:
    """Get all users from the given edition"""

    a1 = aliased(UserRole)
    coaches = db.execute(select(User).join(a1, User.user_id == UserRole.user_id).where(a1.edition_id == edition_id))
    #admins = db.execute(select(User)) TODO: admins

    return coaches #+ admins

