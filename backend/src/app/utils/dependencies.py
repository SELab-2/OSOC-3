from fastapi import Depends
from sqlalchemy.orm import Session

from src.database.crud.editions import get_edition_by_id
from src.database.database import get_session
from src.database.models import Edition


# TODO: Might be nice to use a more descriptive year number here than primary id.
def get_edition(edition_id: int, db: Session = Depends(get_session)) -> Edition:
    """Get an edition from the database, given the id in the path"""
    return get_edition_by_id(db, edition_id)
