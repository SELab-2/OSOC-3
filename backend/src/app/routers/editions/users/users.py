from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.app.routers.tags import Tags
import src.app.logic.users as logic
from src.app.schemas.users import UsersListResponse, StatusBody, RequestAnswer
from src.database.database import get_session


users_router = APIRouter(prefix="/users", tags=[Tags.USERS])





@users_router.post("/{user_id}/request", status_code=204)
async def handle_user_request(edition_id: int, user_id: int, answer: RequestAnswer, db: Session = Depends(get_session)):
    """
    Accept or decline the pending invite request for a given user.
    """

    logic.handle_user_request(db, edition_id, user_id, answer)


