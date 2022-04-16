import base64

from sqlalchemy.orm import Session

import settings
import src.database.crud.invites as crud
from src.app.schemas.invites import InvitesLinkList, EmailAddress, NewInviteLink, InviteLink as InviteLinkModel
from src.app.utils.mailto import generate_mailto_string
from src.database.models import Edition, InviteLink as InviteLinkDB


def delete_invite_link(db: Session, invite_link: InviteLinkDB):
    """Delete an invite link from the database"""
    crud.delete_invite_link(db, invite_link)


def get_pending_invites_page(db: Session, edition: Edition, page: int) -> InvitesLinkList:
    """
    Query the database for a list of invite links
    and wrap the result in a pydantic model
    """
    invites_orm = crud.get_pending_invites_for_edition_page(db, edition, page)
    invites = []
    for invite in invites_orm:
        new_invite = InviteLinkModel(invite_link_id=invite.invite_link_id,
                                     uuid=invite.uuid, target_email=invite.target_email, edition_name=edition.name)
        invites.append(new_invite)
    return InvitesLinkList(invite_links=invites)


def create_mailto_link(db: Session, edition: Edition, email_address: EmailAddress) -> NewInviteLink:
    """Add a new invite link into the database & return a mailto link for it"""
    # Create db entry
    new_link_db = crud.create_invite_link(db, edition, email_address.email)

    # Add edition name & encode with base64
    encoded_uuid = f"{new_link_db.edition.name}/{new_link_db.uuid}".encode("ascii")
    encoded_link = base64.b64encode(encoded_uuid).decode("ascii")

    # Create endpoint for the user to click on
    link = f"{settings.FRONTEND_URL}/register/{encoded_link}"

    return NewInviteLink(mail_to=generate_mailto_string(
        recipient=email_address.email, subject=f"Open Summer Of Code {edition.year} invitation",
        body=link
    ), invite_link=link)
