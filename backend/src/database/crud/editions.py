from sqlalchemy import exc, func, select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

from src.app.exceptions.crud import DuplicateInsertException
from src.app.schemas.editions import EditionBase
from src.database.models import Edition
from .util import paginate


async def get_edition_by_name(db: AsyncSession, edition_name: str) -> Edition:
    """Get an edition given its name

    Args:
        db (Session): connection with the database.
        edition_name (str): the name of the edition you want to find

    Returns:
        Edition: an edition if found else an exception is raised
    """
    query = select(Edition).where(Edition.name == edition_name).order_by(desc(Edition.edition_id))
    result = await db.execute(query)
    return result.scalars().one()


def _get_editions_query() -> Select:
    return select(Edition).order_by(desc(Edition.edition_id))


async def get_editions(db: AsyncSession) -> list[Edition]:
    """Returns a list of all editions"""
    result = await db.execute(_get_editions_query())
    return result.scalars().all()


async def get_editions_page(db: AsyncSession, page: int) -> list[Edition]:
    """Returns a paginated list of all editions"""
    result = await db.execute(paginate(_get_editions_query(), page))
    return result.scalars().all()


async def create_edition(db: AsyncSession, edition: EditionBase) -> Edition:
    """ Create a new edition.

    Args:
        db (Session): connection with the database.
        edition (EditionBase): an edition that needs to be created

    Returns:
        Edition: the newly made edition object.
    """
    new_edition: Edition = Edition(year=edition.year, name=edition.name)
    db.add(new_edition)
    try:
        await db.commit()
        await db.refresh(new_edition)
        return new_edition
    except exc.SQLAlchemyError as exception:
        raise DuplicateInsertException(exception) from exception


async def delete_edition(db: AsyncSession, edition_name: str):
    """Delete an edition.

    Args:
        db (Session): connection with the database.
        edition_name (str): the primary key of the edition that needs to be deleted
    """
    await db.delete(await get_edition_by_name(db, edition_name))
    await db.commit()


async def latest_edition(db: AsyncSession) -> Edition:
    """Returns the latest edition from the database"""
    subquery = select(func.max(Edition.edition_id))
    result = await db.execute(subquery)
    max_edition_id = result.scalar()

    query = select(Edition).where(Edition.edition_id == max_edition_id)
    result2 = await db.execute(query)
    return result2.scalars().one()
