from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.app.routers.tags import Tags
from src.app.schemas.invites import InviteLink, InvitesListResponse
from src.app.utils.dependencies import get_edition
from src.database.crud.invites import get_all_pending_invites
from src.database.database import get_session
from src.database.models import Edition

invites_router = APIRouter(prefix="/invites", tags=[Tags.INVITES])


@invites_router.get("/", response_model=InvitesListResponse)
async def get_invites(edition: Edition = Depends(get_edition), db: Session = Depends(get_session)):
    """
    Get a list of all pending invitation links.
    """
    invites_orm = get_all_pending_invites(db, edition)
    return InvitesListResponse(invite_links=invites_orm)


@invites_router.post("/")
async def create_invite(edition_id: int):
    """
    Create a new invitation link for the current edition.
    """


@invites_router.delete("/{invite_id}")
async def delete_invite(edition_id: int, invite_id: int):
    """
    Delete an existing invitation link manually so that it can't be used anymore.
    """


@invites_router.get("/{invite_id}")
async def get_invite(edition_id: int, invite_id: int):
    """
    Get a specific invitation link to see if it exists or not. Can be used to verify the validity
    of a link before granting a user access to the registration page.
    """
