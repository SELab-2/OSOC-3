from sqlalchemy import update, delete, insert

from src.database.enums import RoleEnum
from src.database.models import User, user_editions, CoachRequest
from sqlalchemy.orm import Session


def get_users_from_edition(db: Session, edition_id: int) -> list[User]:
    """
    Get all users from the given edition
    """

    coaches = db.query(User).join(UserRole).where(UserRole.edition_id == edition_id).all()
    # TODO: admins (depends on changes in db)

    return coaches


def add_user_as_coach(db, edition_id, user_id):
    """
    Add user as admin for the given edition if not already coach
    """

    stmt = (
        insert(user_editions).
        values(user_id=user_id, edition_id=edition_id)
    )
    db.execute(stmt)


def delete_user_as_coach(db, edition_id, user_id):
    """
    Add user as admin for the given edition if not already coach
    """

    stmt = (
        delete(user_editions).
        where(user_id == user_id, edition_id == edition_id)
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

