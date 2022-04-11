from sqlalchemy.orm import Session, Query

from src.database.crud.editions import get_edition_by_name
from src.database.crud.util import paginate
from src.database.models import user_editions, User, Edition, CoachRequest, AuthGoogle, AuthEmail, AuthGitHub
from src.database.crud.editions import get_editions


def _get_admins_query(db: Session, name: str = "") -> Query:
    return db.query(User) \
        .where(User.admin) \
        .where(User.name.contains(name)) \
        .join(AuthEmail, isouter=True) \
        .join(AuthGitHub, isouter=True) \
        .join(AuthGoogle, isouter=True)


def get_admins(db: Session) -> list[User]:
    """
    Get all admins
    """
    return _get_admins_query(db).all()


def get_admins_page(db: Session, page: int, name: str = "") -> list[User]:
    """
    Get all admins paginated
    """
    return paginate(_get_admins_query(db, name), page).all()


def _get_users_query(db: Session, name: str = "") -> Query:
    return db.query(User).where(User.name.contains(name))


def get_users(db: Session) -> list[User]:
    """Get all users (coaches + admins)"""
    return _get_users_query(db).all()


def get_users_page(db: Session, page: int, name: str = "") -> list[User]:
    """Get all users (coaches + admins) paginated"""
    return paginate(_get_users_query(db, name), page).all()


def get_user_edition_names(db: Session, user: User) -> list[str]:
    """Get all names of the editions this user can see"""
    # For admins: return all editions - otherwise, all editions this user is verified coach in
    source = user.editions if not user.admin else get_editions(db)

    editions = []
    # Name is non-nullable in the database, so it can never be None,
    # but MyPy doesn't seem to grasp that concept just yet so we have to check it
    # Could be a oneliner/list comp but that's a bit less readable
    for edition in source:
        if edition.name is not None:
            editions.append(edition.name)

    return editions


def _get_users_for_edition_query(db: Session, edition: Edition, name="") -> Query:
    return db \
        .query(User) \
        .where(User.name.contains(name)) \
        .join(user_editions) \
        .filter(user_editions.c.edition_id == edition.edition_id)


def get_users_for_edition(db: Session, edition_name: str) -> list[User]:
    """
    Get all coaches from the given edition
    """
    return _get_users_for_edition_query(db, get_edition_by_name(db, edition_name)).all()


def get_users_for_edition_page(db: Session, edition_name: str, page: int, name="") -> list[User]:
    """
    Get all coaches from the given edition
    """
    return paginate(_get_users_for_edition_query(db, get_edition_by_name(db, edition_name), name), page).all()


def get_users_for_edition_exclude_edition_page(db: Session, page: int, exclude_edition_name: str, edition_name: str,
                                               name: str) -> list[User]:
    """
    Get all coaches from the given edition except those who are coach in the excluded edition
    """

    exclude_edition = get_edition_by_name(db, exclude_edition_name)

    return paginate(
                _get_users_for_edition_query(db, get_edition_by_name(db, edition_name), name)
                .filter(User.user_id.not_in(
                    db.query(user_editions.c.user_id).where(user_editions.c.edition_id == exclude_edition.edition_id)
                    )
                )
        , page).all()


def get_users_exclude_edition_page(db: Session, page: int, exclude_edition: str, name: str) -> list[User]:
    """
    Get all users who are not coach in the given edition
    """

    edition = get_edition_by_name(db, exclude_edition)

    return paginate(
        db
            .query(User)
            .where(User.name.contains(name))
            .filter(
                User.user_id.not_in(
                    db.query(user_editions.c.user_id).where(user_editions.c.edition_id == edition.edition_id)
                )
            )
        , page).all()


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
