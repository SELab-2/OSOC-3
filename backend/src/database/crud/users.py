from src.database.models import user_editions, User, Edition
from sqlalchemy.orm import Session


def get_all_admins(db: Session) -> list[User]:
    """
    Get all admins
    """

    return db.query(User).where(User.admin).all()


def get_all_users(db: Session) -> list[User]:
    """
    Get all users (coaches + admins)
    """

    return db.query(User).all()


def get_users_from_edition(db: Session, edition_id: int) -> list[User]:
    """
    Get all coaches from the given edition
    """

    return db.query(User).join(user_editions).filter(user_editions.c.edition_id == edition_id).all()


def get_admins_from_edition(db: Session, edition_id: int) -> list[User]:
    """
    Get all admins from the given edition
    """

    return db.query(User).where(User.admin).join(user_editions).filter(user_editions.c.edition_id == edition_id).all()


def edit_admin_status(db: Session, user_id: int, admin: bool):
    """
    Edit the admin-status of a user
    """

    user = db.query(User).where(User.user_id == user_id).one()
    user.admin = admin
    db.add(user)
    db.commit()


def add_coach(db, user_id, edition_id):
    """
    Add user as admin for the given edition
    """

    user = db.query(User).where(User.user_id == user_id).one()
    edition = db.query(Edition).where(Edition.edition_id == edition_id).one()
    user.editions.append(edition)


def remove_coach(db, user_id, edition_id):
    """
    Remove user as admin for the given edition
    """

    db.execute(user_editions.delete(), {"user_id": user_id, "edition_id": edition_id})


def delete_user_as_coach(db, edition_id, user_id):
    """
    Add user as admin for the given edition if not already coach
    """

    user = db.query(User).where(User.user_id == user_id).one()
    edition = db.query(Edition).where(Edition.edition_id == edition_id).one()
    user.editions.remove(edition)
