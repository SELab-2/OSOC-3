from uuid import UUID

import sqlalchemy.exc
from sqlalchemy.orm import Session

from src.app.exceptions.parsing import MalformedUUIDError
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


def get_invite_link_by_uuid(db: Session, invite_uuid: str | UUID) -> InviteLink:
    """Get an invite link by its id
    As the ids are auto-generated per row, there's no need to use the Edition
    from the path parameters as an extra filter
    """
    # Convert to UUID if necessary
    if isinstance(invite_uuid, str):
        try:
            invite_uuid = UUID(invite_uuid)
        except ValueError as value_error:
            # If conversion failed, then the input string was not a valid uuid
            raise MalformedUUIDError(str(invite_uuid)) from value_error

    return db.query(InviteLink).where(InviteLink.uuid == invite_uuid).one()
