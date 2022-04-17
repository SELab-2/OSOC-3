from sqlalchemy.orm import Session, Query

from src.database.crud.editions import get_edition_by_name
from src.database.crud.editions import get_editions
from src.database.crud.util import paginate
from src.database.models import user_editions, User, Edition, CoachRequest, AuthEmail, AuthGitHub, AuthGoogle


def get_user_edition_names(db: Session, user: User) -> list[str]:
    """Get all names of the editions this user can see"""
    # For admins: return all editions - otherwise, all editions this user is verified coach in
    source = user.editions if not user.admin else get_editions(db)

    editions = []
    # Name & year are non-nullable in the database, so it can never be None,
    # but MyPy doesn't seem to grasp that concept just yet so we have to check it
    # Could be a oneliner/list comp but that's a bit less readable
    # Return from newest to oldest
    for edition in sorted(source, key=lambda e: e.year or -1, reverse=True):
        if edition.name is not None:
            editions.append(edition.name)

    return editions


def get_users_filtered_page(
        db: Session,
        admin: bool | None = None,
        edition_name: str | None = None,
        exclude_edition_name: str | None = None,
        name: str | None = None,
        page: int = 0
):
    """
    Get users and filter by optional parameters:
    :param admin: only return admins / only return non-admins
    :param edition_name: only return users who are coach of the given edition
    :param exclude_edition_name: only return users who are not coach of the given edition
    :param name: a string which the user's name must contain
    :param page: the page to return

    Note: When the admin parameter is set, edition_name and exclude_edition_name will be ignored.
    """

    query = db.query(User)

    if name is not None:
        query = query.where(User.name.contains(name))

    if admin is not None:
        query = query.filter(User.admin.is_(admin))
        # If admin parameter is set, edition & exclude_edition is ignored
        return paginate(query, page).all()

    if edition_name is not None:
        edition = get_edition_by_name(db, edition_name)

        query = query \
            .join(user_editions) \
            .filter(user_editions.c.edition_id == edition.edition_id)

    if exclude_edition_name is not None:
        exclude_edition = get_edition_by_name(db, exclude_edition_name)

        query = query.filter(
                User.user_id.not_in(
                    db.query(user_editions.c.user_id).where(user_editions.c.edition_id == exclude_edition.edition_id)
                )
            )

    return paginate(query, page).all()


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


def _get_requests_query(db: Session, user_name: str = "") -> Query:
    return db.query(CoachRequest).join(User).where(User.name.contains(user_name))


def get_requests(db: Session) -> list[CoachRequest]:
    """
    Get all userrequests
    """
    return _get_requests_query(db).all()


def get_requests_page(db: Session, page: int, user_name: str = "") -> list[CoachRequest]:
    """
    Get all userrequests
    """
    return paginate(_get_requests_query(db, user_name), page).all()


def _get_requests_for_edition_query(db: Session, edition: Edition, user_name: str = "") -> Query:
    return db.query(CoachRequest)\
        .where(CoachRequest.edition_id == edition.edition_id)\
        .join(User)\
        .where(User.name.contains(user_name))\
        .join(AuthEmail, isouter=True)\
        .join(AuthGitHub, isouter=True)\
        .join(AuthGoogle, isouter=True)


def get_requests_for_edition(db: Session, edition_name: str = "") -> list[CoachRequest]:
    """
    Get all userrequests from a given edition
    """
    return _get_requests_for_edition_query(db, get_edition_by_name(db, edition_name)).all()


def get_requests_for_edition_page(
        db: Session,
        edition_name: str,
        page: int,
        user_name: str = ""
) -> list[CoachRequest]:
    """
    Get all userrequests from a given edition
    """
    return paginate(_get_requests_for_edition_query(db, get_edition_by_name(db, edition_name), user_name), page).all()


def accept_request(db: Session, request_id: int):
    """
    Remove request and add user as coach
    """
    request = db.query(CoachRequest).where(CoachRequest.request_id == request_id).one()
    edition = db.query(Edition).where(Edition.edition_id == request.edition_id).one()
    add_coach(db, request.user_id, edition.name)
    db.query(CoachRequest).where(CoachRequest.request_id == request_id).delete()
    db.commit()


def reject_request(db: Session, request_id: int):
    """
    Remove request
    """
    db.query(CoachRequest).where(CoachRequest.request_id == request_id).delete()
    db.commit()


def get_user_by_email(db: Session, email: str) -> User:
    """Find a user by their email address"""
    auth_email = db.query(AuthEmail).where(AuthEmail.email == email).one()
    return db.query(User).where(User.user_id == auth_email.user_id).one()


def get_user_by_id(db: Session, user_id: int) -> User:
    """Find a user by their id"""
    return db.query(User).where(User.user_id == user_id).one()
