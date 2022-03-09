from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import Response

from src.app.logic.invites import create_mailto_link, delete_invite_link, get_pending_invites_list
from src.app.routers.tags import Tags
from src.app.schemas.invites import InvitesListResponse, EmailAddress, MailtoLink
from src.app.utils.dependencies import get_edition, get_invite_link
from src.database.database import get_session
from src.database.models import Edition, InviteLink

invites_router = APIRouter(prefix="/invites", tags=[Tags.INVITES])


@invites_router.get("/", response_model=InvitesListResponse)
async def get_invites(db: Session = Depends(get_session), edition: Edition = Depends(get_edition)):
    """
    Get a list of all pending invitation links.
    """
    return get_pending_invites_list(db, edition)


@invites_router.post("/", response_model=MailtoLink)
async def create_invite(email: EmailAddress, db: Session = Depends(get_session), edition: Edition = Depends(get_edition)):
    """
    Create a new invitation link for the current edition.
    """
    return create_mailto_link(db, edition, email)


@invites_router.delete("/{invite_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_invite(invite_link: InviteLink = Depends(get_invite_link), db: Session = Depends(get_session)):
    """
    Delete an existing invitation link manually so that it can't be used anymore.
    """
    delete_invite_link(db, invite_link)


@invites_router.get("/{invite_id}")
async def get_invite(edition_id: int, invite_id: int):
    """
    Get a specific invitation link to see if it exists or not. Can be used to verify the validity
    of a link before granting a user access to the registration page.
    """
