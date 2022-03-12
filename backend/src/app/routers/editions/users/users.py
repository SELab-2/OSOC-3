from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.app.routers.tags import Tags
import src.app.logic.users as logic
from src.app.schemas.users import UsersListResponse, StatusBody, RequestAnswer
from src.database.database import get_session


users_router = APIRouter(prefix="/users", tags=[Tags.USERS])


@users_router.get("/", response_model=UsersListResponse)
async def get_users(edition_id: int, db: Session = Depends(get_session)):
    """
    Get a list of all users from given edition.
    """

    return logic.get_users_list(db, edition_id)


@users_router.post("/{user_id}/coach", status_code=204)
async def add_user_as_coach(edition_id: int, user_id, int, db: Session = Depends(get_session)):
    """
    Add user as coach for the given edition
    """

    logic.add_user_as_coach(db, edition_id, user_id)


@users_router.delete("/{user_id}/coach", status_code=204)
async def delete_user_as_coach(edition_id: int, user_id, int, db: Session = Depends(get_session)):
    """
    Remove user as coach for the given edition
    """

    logic.delete_user_as_coach(db, edition_id, user_id)


@users_router.post("/{user_id}/request", status_code=204)
async def handle_user_request(edition_id: int, user_id: int, answer: RequestAnswer, db: Session = Depends(get_session)):
    """
    Accept or decline the pending invite request for a given user.
    Accept will add the user as coach to the edition
    """

    logic.handle_user_request(db, edition_id, user_id, answer)
