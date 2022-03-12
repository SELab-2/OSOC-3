from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.app.routers.tags import Tags
import src.database.crud.users as crud_users
from src.app.schemas.users import UsersListResponse, StatusBody
from src.database.database import get_session


users_router = APIRouter(prefix="/users", tags=[Tags.USERS])


@users_router.get("/", response_model=UsersListResponse)
async def get_users(edition_id: int, db: Session = Depends(get_session)):
    """
    Get a list of all users from given edition.
    """
    users = crud_users.get_users_from_edition(db, edition_id)

    return users


@users_router.patch("/{user_id}/status")
async def update_user_status(edition_id: int, user_id: int, status: StatusBody, db: Session = Depends(get_session)):
    """
    Update the status of a user (admin/coach/disabled) for a given edition.
    """
    return crud_users.update_user_status(db, edition_id, user_id, status.status)


@users_router.post("/{user_id}/request")
async def handle_user_request(edition_id: int, user_id: int):
    """
    Accept or decline the pending invite request for a given user.
    """
