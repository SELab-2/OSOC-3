from sqlalchemy.orm import Session

from src.database.models import Edition, InviteLink


def create_invite_link(db: Session, edition: Edition, email_address: str) -> InviteLink:
    """Create a new invite link"""
    link = InviteLink(target_email=email_address, edition=edition)
    db.add(link)
    db.commit()
    return link


def get_all_pending_invites(db: Session, edition: Edition) -> list[InviteLink]:
    """Return a list of all invite links in a given edition"""
    return db.query(InviteLink).where(InviteLink.edition == edition).all()
