from sqlalchemy.orm import Session, Query

from src.database.crud.editions import get_edition_by_name
from src.database.crud.util import paginate
from src.database.models import user_editions, User, Edition, CoachRequest, AuthGoogle, AuthEmail, AuthGitHub


def get_admins(db: Session) -> list[User]:
    """
    Get all admins
    """

    return db.query(User) \
        .where(User.admin) \
        .join(AuthEmail, isouter=True) \
        .join(AuthGitHub, isouter=True) \
        .join(AuthGoogle, isouter=True) \
        .all()


def _get_users_query(db: Session) -> Query:
    return db.query(User)


def get_users(db: Session) -> list[User]:
    """Get all users (coaches + admins)"""
    return _get_users_query(db).all()


def get_users_page(db: Session, page: int) -> list[User]:
    """Get all users (coaches + admins) paginated"""
    return paginate(_get_users_query(db), page).all()


def get_user_edition_names(user: User) -> list[str]:
    """Get all names of the editions this user is coach in"""
    # Name is non-nullable in the database, so it can never be None,
    # but MyPy doesn't seem to grasp that concept just yet so we have to check it
    # Could be a oneliner/list comp but that's a bit less readable
    editions = []
    for edition in user.editions:
        if edition.name is not None:
            editions.append(edition.name)

    return editions


def _get_users_for_edition_query(db: Session, edition: Edition) -> Query:
    return db.query(User).join(user_editions).filter(user_editions.c.edition_id == edition.edition_id)


def get_users_for_edition(db: Session, edition_name: str) -> list[User]:
    """
    Get all coaches from the given edition
    """
    return _get_users_for_edition_query(db, get_edition_by_name(db, edition_name)).all()


def get_users_for_edition_page(db: Session, edition_name: str, page: int) -> list[User]:
    """
    Get all coaches from the given edition
    """
    return paginate(_get_users_for_edition_query(db, get_edition_by_name(db, edition_name)), page).all()


def _get_admins_for_edition_query(db: Session, edition: Edition) -> Query:
    return db.query(User) \
        .where(User.admin) \
        .join(user_editions) \
        .filter(user_editions.c.edition_id == edition.edition_id)


def get_admins_for_edition(db: Session, edition_name: str) -> list[User]:
    """
    Get all admins from the given edition
    """
    return _get_admins_for_edition_query(db, get_edition_by_name(db, edition_name)).all()


def get_admins_for_edition_page(db: Session, edition_name: str, page: int) -> list[User]:
    """
    Get all admins from the given edition
    """
    return paginate(_get_admins_for_edition_query(db, get_edition_by_name(db, edition_name)), page).all()


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
    db.commit()


def remove_coach(db: Session, user_id: int, edition_name: str):
    """
    Remove user as coach for the given edition
    """
    edition = db.query(Edition).where(Edition.name == edition_name).one()
    db.query(user_editions) \
        .where(user_editions.c.user_id == user_id) \
        .where(user_editions.c.edition_id == edition.edition_id) \
        .delete()
    db.commit()


def remove_coach_all_editions(db: Session, user_id: int):
    """
    Remove user as coach from all editions
    """
    db.query(user_editions).where(user_editions.c.user_id == user_id).delete()
    db.commit()


def _get_requests_query(db: Session) -> Query:
    return db.query(CoachRequest).join(User)


def get_requests(db: Session) -> list[CoachRequest]:
    """
    Get all userrequests
    """
    return _get_requests_query(db).all()


def get_requests_page(db: Session, page: int) -> list[CoachRequest]:
    """
    Get all userrequests
    """
    return paginate(_get_requests_query(db), page).all()


def _get_requests_for_edition_query(db: Session, edition: Edition) -> Query:
    return db.query(CoachRequest).where(CoachRequest.edition_id == edition.edition_id).join(User)


def get_requests_for_edition(db: Session, edition_name: str) -> list[CoachRequest]:
    """
    Get all userrequests from a given edition
    """
    return _get_requests_for_edition_query(db, get_edition_by_name(db, edition_name)).all()


def get_requests_for_edition_page(db: Session, edition_name: str, page: int) -> list[CoachRequest]:
    """
    Get all userrequests from a given edition
    """
    return paginate(_get_requests_for_edition_query(db, get_edition_by_name(db, edition_name)), page).all()


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
