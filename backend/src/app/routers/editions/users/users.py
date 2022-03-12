from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.app.routers.tags import Tags
import src.app.logic.users as logic
from src.app.schemas.users import UsersListResponse, StatusBody
from src.database.database import get_session


users_router = APIRouter(prefix="/users", tags=[Tags.USERS])


@users_router.get("/", response_model=UsersListResponse)
async def get_users(edition_id: int, db: Session = Depends(get_session)):
    """
    Get a list of all users from given edition.
    """

    return logic.get_users_list(db, edition_id)


@users_router.patch("/{user_id}/status", status_code=204)
async def update_user_status(edition_id: int, user_id: int, status: StatusBody, db: Session = Depends(get_session)):
    """
    Update the status of a user (admin/coach/disabled) for a given edition.
    """

    logic.update_user_status(db, edition_id, user_id, status.status)


@users_router.post("/{user_id}/request")
async def handle_user_request(edition_id: int, user_id: int):
    """
    Accept or decline the pending invite request for a given user.
    """
