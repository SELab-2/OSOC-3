from sqlalchemy import update, delete, insert

from src.database.enums import RoleEnum
from src.database.models import User, UserRole, CoachRequest
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


def accept_request(db: Session, edition_id: int, user_id: int):
    """
    Accept a coach request:
        - Remove the request
        - Add user as admin to given edition
    """
    stmt = (
        delete(CoachRequest).
        where(user_id == user_id)
    )
    db.execute(stmt)

    stmt = (
        insert(UserRole).
        values(user_id=user_id, role=RoleEnum.COACH, edition_id=edition_id)
    )
    db.execute(stmt)


def reject_request(db: Session, user_id: int):
    stmt = (
        delete(CoachRequest).
        where(user_id == user_id)
    )

    db.execute(stmt)
