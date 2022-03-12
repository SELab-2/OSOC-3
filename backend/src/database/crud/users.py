from sqlalchemy import update

from src.database.enums import RoleEnum
from src.database.models import User, UserRole
from sqlalchemy.orm import Session


def get_users_from_edition(db: Session, edition_id: int) -> list[User]:
    """
    Get all users from the given edition
    """

    coaches = db.query(User).join(UserRole).where(UserRole.edition_id == edition_id).all()
    # TODO: admins (depends on changes in db)

    return coaches


def update_user_status(db: Session, edition_id: int, user_id: int, status: RoleEnum):
    """
    Change the status of a given user for a given edition
    """
    stmt = (
        update(UserRole).
        where(UserRole.user_id == user_id).
        where(UserRole.edition_id == edition_id).
        values({UserRole.role: status})
    )

    db.execute(stmt)




