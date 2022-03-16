from sqlalchemy.orm import Session

from src.app.schemas.editions import Edition, EditionBase, EditionList
import src.database.crud.editions as crud_editions 
from src.database.models import Edition

def get_editions(db: Session) -> EditionList:
    """Get a list of all editions.

    Args:
        db (Session): connection with the database.

    Returns:
        EditionList: an object with a list of all the editions.
    """
    return EditionList(editions=crud_editions.get_editions(db))


def get_edition_by_id(db: Session, edition_id: int) -> Edition:
    """Get a specific edition.

    Args:
        db (Session): connection with the database.

    Returns:
        Edition: an edition.
    """
    return crud_editions.get_edition_by_id(db, edition_id)


def create_edition(db: Session, edition: EditionBase) -> Edition:
    """ Create a new edition.

    Args:
        db (Session): connection with the database.

    Returns:
        Edition: the newly made edition object.
    """
    crud_editions.create_edition(db, edition)


def delete_edition(db: Session, edition_id: int):
    """Delete an existing edition.

    Args:
        db (Session): connection with the database.
        edition_id (int): the id of the edition that needs to be deleted, if found.

    Returns: nothing
    """
    crud_editions.delete_edition(db, edition_id)
