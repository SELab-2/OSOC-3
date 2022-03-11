from sqlalchemy.orm import Session
from src.database.models import Edition
from src.app.schemas.editions import EditionBase
from typing import List, Optional


def get_edition_by_key(db: Session, edition_id: int) -> Optional[Edition]:
    """Get an edition given its primary key

    Args:
        db (Session): connection with the database.
        edition_id (int): the primary key of the edition you want to find

    Returns:
        Optional(Edition): an edition if found else None
    """
    return db.get(Edition, edition_id)


def get_editions(db: Session) -> List[Edition]:
    """Get a list of all editions.

    Args:
        db (Session): connection with the database.

    Returns:
        List[Edition]: a list of all the editions.
    """
    return db.query(Edition).all()


def create_edition(db: Session, edition: EditionBase) -> Optional[Edition]:
    """ Create a new edition.

    Args:
        db (Session): connection with the database.
        edition (EditionBase): an edition that needs to be created

    Returns:
        Edition: the newly made edition object.
    """
    new_edition: Edition = Edition()
    new_edition.year = edition.year
    db.add(new_edition)
    try:
        db.commit()
        db.refresh(new_edition)
        return new_edition
    except Exception:
        db.rollback()
        return None

def delete_edition(db: Session, edition_id: int) -> bool:
    """Delete an edition.

    Args:
        db (Session): connection with the database.
        edition_id (int): the primary key of the edition that needs to be deleted

    Returns:
        bool: True if the edition was found and deleted, False if the edition was not found
    """
    edition_to_delete = get_edition_by_key(db, edition_id)
    if edition_to_delete is not None:
        db.delete(edition_to_delete)
        db.commit()
        return True
    else: return False
