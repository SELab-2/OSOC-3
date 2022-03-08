from sqlalchemy.orm import Session

from src.database.models import Edition, InviteLink


def get_all_pending_invites(db: Session, edition: Edition) -> list[InviteLink]:
    """
    Return a list of all invite links in a given edition
    """
    return db.query(InviteLink).where(InviteLink.edition == edition).all()
