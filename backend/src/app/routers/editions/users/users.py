from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.app.routers.tags import Tags
from src.database.crud.users import get_users_from_edition
from src.database.database import get_session
from src.database.models import User


users_router = APIRouter(prefix="/users", tags=[Tags.USERS])


class UserBase(BaseModel):
    user_id: int
    name: str
    email: str


@users_router.get("/", response_model=list[UserBase])
async def get_users(edition_id: int, db: Session = Depends(get_session)) -> list[User]:
    """Get a list of all users from given edition."""
    return get_users_from_edition(db, edition_id)


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
