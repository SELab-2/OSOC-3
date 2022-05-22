import base64

from sqlalchemy.ext.asyncio import AsyncSession

import settings
import src.database.crud.invites as crud
from src.app.schemas.invites import InvitesLinkList, EmailAddress, NewInviteLink
from src.app.utils.mailto import generate_mailto_string
from src.database.models import Edition, InviteLink as InviteLinkDB


async def delete_invite_link(db: AsyncSession, invite_link: InviteLinkDB):
    """Delete an invite link from the database"""
    await crud.delete_invite_link(db, invite_link)


async def get_pending_invites_page(db: AsyncSession, edition: Edition, page: int) -> InvitesLinkList:
    """Query the database for a list of invite links and wrap the result in a pydantic model"""
    invite_page = await crud.get_pending_invites_for_edition_page(db, edition, page)
    return InvitesLinkList(invite_links=invite_page)


async def create_mailto_link(db: AsyncSession, edition: Edition, email_address: EmailAddress) -> NewInviteLink:
    """Add a new invite link into the database & return a mailto link for it"""
    # Create db entry, drop existing.
    invite = await crud.get_optional_invite_link_by_edition_and_email(db, edition, email_address.email)
    if invite is None:
        invite = await crud.create_invite_link(db, edition, email_address.email)

    # Add edition name & encode with base64
    encoded_uuid = f"{invite.edition.name}/{invite.uuid}".encode("utf-8")
    encoded_link = base64.b64encode(encoded_uuid).decode("utf-8")

    # Create endpoint for the user to click on
    link = f"{settings.FRONTEND_URL}/register/{encoded_link}"

    with open('templates/invites.txt', 'r', encoding="utf-8") as file:
        message = file.read().format(invite_link=link)

    return NewInviteLink(mail_to=generate_mailto_string(
        recipient=email_address.email, subject=f"Open Summer Of Code {edition.year} invitation",
        body=message
    ), invite_link=link)
