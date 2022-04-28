from uuid import UUID

from sqlalchemy.orm import Session, Query

from src.app.exceptions.parsing import MalformedUUIDError
from src.database.crud.util import paginate
from src.database.models import Edition, InviteLink


def create_invite_link(db: Session, edition: Edition, email_address: str) -> InviteLink:
    """Create a new invite link"""
    link = InviteLink(target_email=email_address, edition=edition)
    db.add(link)
    db.commit()
    return link


def delete_invite_link(db: Session, invite_link: InviteLink, commit: bool = True):
    """Delete an invite link from the database"""
    db.delete(invite_link)

    if commit:
        db.commit()


def _get_pending_invites_for_edition_query(db: Session, edition: Edition) -> Query:
    """Return the query for all InviteLinks linked to a given edition"""
    return db.query(InviteLink).where(InviteLink.edition == edition).order_by(InviteLink.invite_link_id)


def get_pending_invites_for_edition(db: Session, edition: Edition) -> list[InviteLink]:
    """Returns a list with all InviteLinks linked to a given edition"""
    return _get_pending_invites_for_edition_query(db, edition).all()


def get_pending_invites_for_edition_page(db: Session, edition: Edition, page: int) -> list[InviteLink]:
    """Returns a paginated list with all InviteLinks linked to a given edition"""
    return paginate(_get_pending_invites_for_edition_query(db, edition), page).all()


def get_optional_invite_link_by_edition_and_email(db: Session, edition: Edition, email: str) -> InviteLink | None:
    """Return an optional invite link by edition and target_email"""
    return db\
        .query(InviteLink)\
        .where(InviteLink.edition == edition)\
        .where(InviteLink.target_email == email)\
        .one_or_none()


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
