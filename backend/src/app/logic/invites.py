from sqlalchemy.orm import Session

from src.app.schemas.invites import InvitesListResponse, EmailAddress, NewInviteLink, InviteLink as InviteLinkModel
from src.app.utils.mailto import generate_mailto_string
from src.database.crud.invites import create_invite_link, delete_invite_link as delete_link_db, get_all_pending_invites
from src.database.models import Edition, InviteLink as InviteLinkDB

import settings


def delete_invite_link(db: Session, invite_link: InviteLinkDB):
    """Delete an invite link from the database"""
    delete_link_db(db, invite_link)


def get_pending_invites_list(db: Session, edition: Edition) -> InvitesListResponse:
    """
    Query the database for a list of invite links
    and wrap the result in a pydantic model
    """
    invites_orm = get_all_pending_invites(db, edition)
    invites = []
    for invite in invites_orm:
        new_invite = InviteLinkModel(invite_link_id=invite.invite_link_id,
                                     uuid=invite.uuid, target_email=invite.target_email, edition_name=edition.name)
        invites.append(new_invite)
    return InvitesListResponse(invite_links=invites)


def create_mailto_link(db: Session, edition: Edition, email_address: EmailAddress) -> NewInviteLink:
    """Add a new invite link into the database & return a mailto link for it"""
    # Create db entry
    new_link_db = create_invite_link(db, edition, email_address.email)

    # Create endpoint for the user to click on
    link = f"{settings.FRONTEND_URL}/register/{new_link_db.uuid}"

    return NewInviteLink(mail_to=generate_mailto_string(
        recipient=email_address.email, subject=f"Open Summer Of Code {edition.year} invitation",
        body=link
    ), invite_link=link)
