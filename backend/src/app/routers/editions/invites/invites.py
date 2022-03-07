from fastapi import APIRouter

from src.app.routers.tags import Tags

invites_router = APIRouter(prefix="/invites", tags=[Tags.INVITES])


@invites_router.get("/")
async def get_invites(edition_id: int):
    """
    Get a list of all pending invitation links.
    """


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
