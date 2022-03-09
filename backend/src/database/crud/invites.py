from sqlalchemy.orm import Session

from src.database.models import Edition, InviteLink


def create_invite_link(db: Session, edition: Edition, email_address: str) -> InviteLink:
    """Create a new invite link"""
    link = InviteLink(target_email=email_address, edition=edition)
    db.add(link)
    db.commit()
    return link


def delete_invite_link(db: Session, invite_link: InviteLink):
    """Delete an invite link from the database"""
    db.delete(invite_link)
    db.commit()


def get_all_pending_invites(db: Session, edition: Edition) -> list[InviteLink]:
    """Return a list of all invite links in a given edition"""
    return db.query(InviteLink).where(InviteLink.edition == edition).all()


def get_invite_link_by_id(db: Session, invite_id: int) -> InviteLink:
    """Get an invite link by its id
    As the ids are auto-generated per row, there's no need to use the Edition
    from the path parameters as an extra filter
    """
    return db.query(InviteLink).where(InviteLink.invite_link_id == invite_id).one()
