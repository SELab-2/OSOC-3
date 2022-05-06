from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

from src.app.schemas.users import FilterParameters
from src.database.crud.editions import get_edition_by_name
from src.database.crud.editions import get_editions
from src.database.crud.util import paginate
from src.database.models import user_editions, User, Edition, CoachRequest, AuthEmail, AuthGitHub, AuthGoogle


async def get_user_edition_names(db: AsyncSession, user: User) -> list[str]:
    """Get all names of the editions this user can see"""
    # For admins: return all editions - otherwise, all editions this user is verified coach in
    source = user.editions if not user.admin else await get_editions(db)

    editions = []
    # Name & year are non-nullable in the database, so it can never be None,
    # but MyPy doesn't seem to grasp that concept just yet so we have to check it
    # Could be a oneliner/list comp but that's a bit less readable
    # Return from newest to oldest
    for edition in sorted(source, key=lambda e: e.year or -1, reverse=True):
        if edition.name is not None:
            editions.append(edition.name)

    return editions


async def get_users_filtered_page(db: AsyncSession, params: FilterParameters):
    """
    Get users and filter by optional parameters:
    :param admin: only return admins / only return non-admins
    :param edition_name: only return users who are coach of the given edition
    :param exclude_edition_name: only return users who are not coach of the given edition
    :param name: a string which the user's name must contain
    :param page: the page to return

    Note: When the admin parameter is set, edition_name and exclude_edition_name will be ignored.
    """

    query = select(User)

    if params.name is not None:
        query = query.where(User.name.contains(params.name))

    if params.admin is not None:
        query = query.filter(User.admin.is_(params.admin))
        # If admin parameter is set, edition & exclude_edition is ignored
        return (await db.execute(paginate(query, params.page))).scalars().all()

    if params.edition is not None:
        edition = await get_edition_by_name(db, params.edition)

        query = query \
            .join(user_editions) \
            .filter(user_editions.c.edition_id == edition.edition_id)

    if params.exclude_edition is not None:
        exclude_edition = await get_edition_by_name(db, params.exclude_edition)
        exclude_user_id = select(user_editions.c.user_id)\
            .where(user_editions.c.edition_id == exclude_edition.edition_id)

        query = query.filter(User.user_id.not_in(exclude_user_id))

    return (await db.execute(paginate(query, params.page))).scalars().all()


async def edit_admin_status(db: AsyncSession, user_id: int, admin: bool):
    """
    Edit the admin-status of a user
    """
    result = await db.execute(select(User).where(User.user_id == user_id))
    user = result.scalar_one()
    user.admin = admin
    db.add(user)
    await db.commit()


async def add_coach(db: AsyncSession, user_id: int, edition_name: str):
    """
    Add user as coach for the given edition
    """
    user_result = await db.execute(select(User).where(User.user_id == user_id))
    user = user_result.scalar_one()
    edition_result = await db.execute(select(Edition).where(Edition.name == edition_name))
    edition = edition_result.scalar_one()
    user.editions.append(edition)

    await db.commit()


async def remove_coach(db: AsyncSession, user_id: int, edition_name: str):
    """
    Remove user as coach for the given edition
    """
    edition_result = await db.execute(select(Edition).where(Edition.name == edition_name))
    edition = edition_result.scalar_one()

    delete_query = delete(user_editions) \
        .where(user_editions.c.user_id == user_id) \
        .where(user_editions.c.edition_id == edition.edition_id)
    await db.execute(delete_query)
    await db.commit()


async def remove_coach_all_editions(db: AsyncSession, user_id: int):
    """
    Remove user as coach from all editions
    """
    await db.execute(delete(user_editions).where(user_editions.c.user_id == user_id))
    await db.commit()


def _get_requests_query(user_name: str = "") -> Select:
    return select(CoachRequest).join(User).where(User.name.contains(user_name))


async def get_requests(db: AsyncSession) -> list[CoachRequest]:
    """
    Get all userrequests
    """
    return (await db.execute(_get_requests_query())).scalars().all()


async def get_requests_page(db: AsyncSession, page: int, user_name: str = "") -> list[CoachRequest]:
    """
    Get all userrequests
    """
    return (await db.execute(paginate(_get_requests_query(user_name), page))).scalars().all()


def _get_requests_for_edition_query(edition: Edition, user_name: str = "") -> Select:
    return select(CoachRequest) \
        .where(CoachRequest.edition_id == edition.edition_id) \
        .join(User) \
        .where(User.name.contains(user_name)) \
        .join(AuthEmail, isouter=True) \
        .join(AuthGitHub, isouter=True) \
        .join(AuthGoogle, isouter=True)


async def get_requests_for_edition(db: AsyncSession, edition_name: str = "") -> list[CoachRequest]:
    """
    Get all userrequests from a given edition
    """
    edition = await get_edition_by_name(db, edition_name)
    return (await db.execute(_get_requests_for_edition_query(edition))).scalars().all()


async def get_requests_for_edition_page(
        db: AsyncSession,
        edition_name: str,
        page: int,
        user_name: str = ""
) -> list[CoachRequest]:
    """
    Get all userrequests from a given edition
    """
    edition = await get_edition_by_name(db, edition_name)
    return (await db.execute(paginate(_get_requests_for_edition_query(edition, user_name), page))).scalars().all()


async def accept_request(db: AsyncSession, request_id: int):
    """
    Remove request and add user as coach
    """
    request = (await db.execute(select(CoachRequest).where(CoachRequest.request_id == request_id))).scalar_one()
    edition = (await db.execute(select(Edition).where(Edition.edition_id == request.edition_id))).scalar_one()
    await add_coach(db, request.user_id, edition.name)
    await db.execute(delete(CoachRequest).where(CoachRequest.request_id == request_id))
    await db.commit()


async def reject_request(db: AsyncSession, request_id: int):
    """
    Remove request
    """
    await db.execute(delete(CoachRequest).where(CoachRequest.request_id == request_id))
    await db.commit()


async def remove_request_if_exists(db: AsyncSession, user_id: int, edition_name: str):
    """Remove a pending request for a user if there is one, otherwise do nothing"""
    edition = (await db.execute(select(Edition).where(Edition.name == edition_name))).scalar_one()
    delete_query = delete(CoachRequest).where(CoachRequest.user_id == user_id)\
        .where(CoachRequest.edition_id == edition.edition_id)
    await db.execute(delete_query)
    await db.commit()


async def get_user_by_email(db: AsyncSession, email: str) -> User:
    """Find a user by their email address"""
    auth_email = (await db.execute(select(AuthEmail).where(AuthEmail.email == email))).scalar_one()
    return (await db.execute(select(User).where(User.user_id == auth_email.user_id))).scalar_one()


async def get_user_by_id(db: AsyncSession, user_id: int) -> User:
    """Find a user by their id"""
    query = select(User).where(User.user_id == user_id)
    result = await db.execute(query)
    return result.scalars().one()
