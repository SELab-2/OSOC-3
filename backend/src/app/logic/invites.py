from sqlalchemy.orm import Session

import settings
import src.database.crud.invites as crud
from src.app.schemas.invites import InvitesLinkList, EmailAddress, NewInviteLink
from src.app.utils.mailto import generate_mailto_string
from src.database.models import Edition, InviteLink as InviteLinkDB


def delete_invite_link(db: Session, invite_link: InviteLinkDB):
    """Delete an invite link from the database"""
    crud.delete_invite_link(db, invite_link)


def get_pending_invites_page(db: Session, edition: Edition, page: int) -> InvitesLinkList:
    """Query the database for a list of invite links and wrap the result in a pydantic model"""
    return InvitesLinkList(invite_links=crud.get_pending_invites_for_edition_page(db, edition, page))


def create_mailto_link(db: Session, edition: Edition, email_address: EmailAddress) -> NewInviteLink:
    """Add a new invite link into the database & return a mailto link for it"""
    # Create db entry, drop existing.
    invite = crud.get_optional_invite_link_by_edition_and_email(db, edition, email_address.email)
    if invite is None:
        invite = crud.create_invite_link(db, edition, email_address.email)

    # Create endpoint for the user to click on
    link = f"{settings.FRONTEND_URL}/register/{invite.uuid}"

    return NewInviteLink(mail_to=generate_mailto_string(
        recipient=email_address.email, subject=f"Open Summer Of Code {edition.year} invitation",
        body=link
    ), invite_link=link)
