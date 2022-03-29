from sqlalchemy.orm import Session
from sqlalchemy import exc
from src.app.exceptions.editions import DuplicateInsertException
from src.database.models import Edition
from src.app.schemas.editions import EditionBase


def get_edition_by_id(db: Session, edition_id: int) -> Edition:
    """Get an edition given its primary key

    Args:
        db (Session): connection with the database.
        edition_id (int): the primary key of the edition you want to find

    Returns:
        Edition: an edition if found else an exception is raised
    """
    return db.query(Edition).where(Edition.edition_id == edition_id).one()


def get_editions(db: Session) -> list[Edition]:
    """Get a list of all editions.

    Args:
        db (Session): connection with the database.

    Returns:
        EditionList: an object with a list of all editions
    """
    return db.query(Edition).all()


def create_edition(db: Session, edition: EditionBase) -> Edition:
    """ Create a new edition.

    Args:
        db (Session): connection with the database.
        edition (EditionBase): an edition that needs to be created

    Returns:
        Edition: the newly made edition object.
    """
    new_edition: Edition = Edition(year=edition.year)
    db.add(new_edition)
    try:
        db.commit()
        db.refresh(new_edition)
        return new_edition
    except exc.SQLAlchemyError as exception:
        raise DuplicateInsertException(exception) from exception


def delete_edition(db: Session, edition_id: int):
    """Delete an edition.

    Args:
        db (Session): connection with the database.
        edition_id (int): the primary key of the edition that needs to be deleted
    """
    edition_to_delete = get_edition_by_id(db, edition_id)
    db.delete(edition_to_delete)
    db.commit()
