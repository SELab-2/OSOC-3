from sqlalchemy.orm import Session

from src.database.models import Edition


def get_edition_by_id(database: Session, edition_id: int) -> Edition:
    """Get an edition given its primary key"""
    return database.query(Edition).where(Edition.edition_id == edition_id).one()
