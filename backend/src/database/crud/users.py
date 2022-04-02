from sqlalchemy.orm import Session
from src.database.models import user_editions, User, Edition, CoachRequest


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


def get_user_edition_names(user: User) -> list[str]:
    """Get all names of the editions this user is coach in"""
    return list(map(lambda e: e.name, user.editions))


def get_users_from_edition(db: Session, edition_name: str) -> list[User]:
    """
    Get all coaches from the given edition
    """
    edition = db.query(Edition).where(Edition.name == edition_name).one()
    return db.query(User).join(user_editions).filter(user_editions.c.edition_id == edition.edition_id).all()


def get_admins_from_edition(db: Session, edition_name: str) -> list[User]:
    """
    Get all admins from the given edition
    """
    edition = db.query(Edition).where(Edition.name == edition_name).one()
    return db.query(User).where(User.admin).join(user_editions).filter(user_editions.c.edition_id == edition.edition_id).all()


def edit_admin_status(db: Session, user_id: int, admin: bool):
    """
    Edit the admin-status of a user
    """

    user = db.query(User).where(User.user_id == user_id).one()
    user.admin = admin
    db.add(user)
    db.commit()


def add_coach(db: Session, user_id: int, edition_name: str):
    """
    Add user as coach for the given edition
    """

    user = db.query(User).where(User.user_id == user_id).one()
    edition = db.query(Edition).where(Edition.name == edition_name).one()
    user.editions.append(edition)


def remove_coach(db: Session, user_id: int, edition_name: str):
    """
    Remove user as coach for the given edition
    """
    edition = db.query(Edition).where(Edition.name == edition_name).one()
    db.execute(user_editions.delete(), {"user_id": user_id, "edition_id": edition.edition_id})


def delete_user_as_coach(db: Session, edition_name: str, user_id: int):
    """
    Add user as admin for the given edition if not already coach
    """

    user = db.query(User).where(User.user_id == user_id).one()
    edition = db.query(Edition).where(Edition.name == edition_name).one()
    user.editions.remove(edition)


def get_all_requests(db: Session) -> list[CoachRequest]:
    """
    Get all userrequests
    """

    return db.query(CoachRequest).join(User).all()


def get_all_requests_from_edition(db: Session, edition_name: str) -> list[CoachRequest]:
    """
    Get all userrequests from a given edition
    """
    edition = db.query(Edition).where(Edition.name == edition_name).one()
    return db.query(CoachRequest).where(CoachRequest.edition_id == edition.edition_id).join(User).all()


def accept_request(db: Session, request_id: int):
    """
    Remove request and add user as coach
    """

    request = db.query(CoachRequest).where(CoachRequest.request_id == request_id).one()
    edition = db.query(Edition).where(Edition.edition_id == request.edition_id).one()
    add_coach(db, request.user_id, edition.name)
    db.query(CoachRequest).where(CoachRequest.request_id == request_id).delete()


def reject_request(db: Session, request_id: int):
    """
    Remove request
    """

    db.query(CoachRequest).where(CoachRequest.request_id == request_id).delete()
