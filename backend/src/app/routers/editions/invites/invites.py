from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import Response

from src.app.logic.invites import create_mailto_link, delete_invite_link, get_pending_invites_page
from src.app.routers.tags import Tags
from src.app.utils.dependencies import get_edition, get_invite_link, require_admin, get_editable_edition
from src.app.schemas.invites import InvitesLinkList, EmailAddress, NewInviteLink, InviteLink as InviteLinkModel
from src.database.database import get_session
from src.database.models import Edition, InviteLink as InviteLinkDB

invites_router = APIRouter(prefix="/invites", tags=[Tags.INVITES])


@invites_router.get("", response_model=InvitesLinkList, dependencies=[Depends(require_admin)])
async def get_invites(db: AsyncSession = Depends(get_session), edition: Edition = Depends(get_edition), page: int = 0):
    """
    Get a list of all pending invitation links.
    """
    return await get_pending_invites_page(db, edition, page)


@invites_router.post("", status_code=status.HTTP_201_CREATED, response_model=NewInviteLink,
                     dependencies=[Depends(require_admin)])
async def create_invite(email: EmailAddress, db: AsyncSession = Depends(get_session),
                        edition: Edition = Depends(get_editable_edition)):
    """
    Create a new invitation link for the current edition.
    """
    return await create_mailto_link(db, edition, email)


@invites_router.delete("/{invite_uuid}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response,
                       dependencies=[Depends(require_admin), Depends(get_edition)])
async def delete_invite(invite_link: InviteLinkDB = Depends(get_invite_link), db: AsyncSession = Depends(get_session)):
    """
    Delete an existing invitation link manually so that it can't be used anymore.
    """
    await delete_invite_link(db, invite_link)


@invites_router.get("/{invite_uuid}", response_model=InviteLinkModel, dependencies=[Depends(get_edition)])
async def get_invite(invite_link: InviteLinkDB = Depends(get_invite_link)):
    """
    Get a specific invitation link to see if it exists or not. Can be used to verify the validity
    of a link before granting a user access to the registration page.
    """
    return invite_link
