from fastapi import APIRouter

from src.app.routers.tags import Tags

users_router = APIRouter(prefix="/users", tags=[Tags.USERS])


@users_router.get("/")
async def get_users(edition_id: int):
    """
    Get a list of all users (admins & coaches).
    """


@users_router.patch("/{user_id}/status")
async def update_user_status(edition_id: int, user_id: int):
    """
    Update the status of a user (admin/coach/disabled).
    """


@users_router.post("/{user_id}/request")
async def handle_user_request(edition_id: int, user_id: int):
    """
    Accept or decline the pending invite request for a given user.
    """
