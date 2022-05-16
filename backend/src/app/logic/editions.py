from sqlalchemy.ext.asyncio import AsyncSession

import src.database.crud.editions as crud_editions
from src.app.schemas.editions import EditionBase, EditionList
from src.database.models import Edition as EditionModel


async def get_editions_page(db: AsyncSession, page: int) -> EditionList:
    """Get a paginated list of all editions."""
    editions_page = await crud_editions.get_editions_page(db, page)
    return EditionList(editions=editions_page)


async def get_edition_by_name(db: AsyncSession, edition_name: str) -> EditionModel:
    """Get a specific edition.

    Args:
        db (Session): connection with the database.

    Returns:
        Edition: an edition.
    """
    return await crud_editions.get_edition_by_name(db, edition_name)


async def create_edition(db: AsyncSession, edition: EditionBase) -> EditionModel:
    """ Create a new edition.

    Args:
        db (Session): connection with the database.

    Returns:
        Edition: the newly made edition object.
    """
    return await crud_editions.create_edition(db, edition)


async def delete_edition(db: AsyncSession, edition_name: str):
    """Delete an existing edition.

    Args:
        db (Session): connection with the database.
        edition_name (str): the name of the edition that needs to be deleted, if found.

    Returns: nothing
    """
    await crud_editions.delete_edition(db, edition_name)
