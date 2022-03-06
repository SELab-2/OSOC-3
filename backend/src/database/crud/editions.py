from src.database.models import Edition
from sqlalchemy.orm import Session


def get_edition_by_id(db: Session, edition_id: int) -> Edition:
    """Get an edition given its primary key"""
    return db.query(Edition).where(Edition.edition_id == edition_id).one()
