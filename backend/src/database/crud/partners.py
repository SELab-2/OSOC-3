from sqlalchemy.orm import Session

from src.database.models import Partner


def create_partner(db: Session, name: str, commit: bool = True) -> Partner:
    """Create a partner given a name"""
    partner = Partner(name=name)
    db.add(partner)

    if commit:
        db.flush()

    return partner


def get_optional_partner_by_name(db: Session, name: str) -> Partner | None:
    """Returns a list of all projects from a certain edition from the database"""
    return db.query(Partner).where(Partner.name == name).one_or_none()
