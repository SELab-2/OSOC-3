from sqlalchemy import exc
from sqlalchemy.orm import Query
from sqlalchemy.orm import Session

from src.app.exceptions.editions import DuplicateInsertException
from src.app.schemas.editions import EditionBase
from src.database.models import Edition
from .util import paginate


def get_edition_by_name(db: Session, edition_name: str) -> Edition:
    """Get an edition given its name

    Args:
        db (Session): connection with the database.
        edition_name (str): the name of the edition you want to find

    Returns:
        Edition: an edition if found else an exception is raised
    """
    return db.query(Edition).where(Edition.name == edition_name).one()


def _get_editions_query(db: Session) -> Query:
    return db.query(Edition)


def get_editions(db: Session) -> list[Edition]:
    """Returns a list of all editions"""
    return _get_editions_query(db).all()


def get_editions_page(db: Session, page: int) -> list[Edition]:
    """Returns a paginated list of all editions"""
    return paginate(_get_editions_query(db), page).all()


def create_edition(db: Session, edition: EditionBase) -> Edition:
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
        db.commit()
        db.refresh(new_edition)
        return new_edition
    except exc.SQLAlchemyError as exception:
        raise DuplicateInsertException(exception) from exception


def delete_edition(db: Session, edition_name: str):
    """Delete an edition.

    Args:
        db (Session): connection with the database.
        edition_name (str): the primary key of the edition that needs to be deleted
    """
    edition_to_delete = get_edition_by_name(db, edition_name)
    db.delete(edition_to_delete)
    db.commit()
