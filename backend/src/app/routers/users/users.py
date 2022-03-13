from fastapi import APIRouter, Query, Depends
from requests import Session

from src.app.routers.tags import Tags
import src.app.logic.users as logic
from src.app.schemas.users import UsersListResponse, AdminPatch
from src.database.database import get_session

users_router = APIRouter(prefix="/users", tags=[Tags.USERS])


@users_router.get("/", response_model=UsersListResponse)
async def get_users(admin: bool = Query(False), edition: int | None = Query(None), db: Session = Depends(get_session)):
    """
    Get a list of all users.
    """

    return logic.get_users_list(db, admin, edition)


""""
/editions/edition_id/users" wordt "/users?edition=edition_id_here"

iemand admin maken/demoten is via "PATCH /users/user_id"

iemand coach maken/removen is via "POST/DELETE /users/user_id/editions/edition_id"

zoeken op admins is via "GET /users?admin=true", de default is false, als je "edition" en "admin=true" opgeeft wordt 
edition als filter genegeerd (bij filters is dat oke, bij /die/path/parameters/ niet echt)
"""


@users_router.patch("/{user_id}", status_code=204)
async def post_edition(user_id: int, admin: AdminPatch, db: Session = Depends(get_session)):
    """
    Set admin-status of user
    """

    logic.edit_admin_status(db, user_id, admin)


@users_router.post("/{user_id}/editions/{edition_id}")
async def delete_edition(user_id: int, edition_id: int, db: Session = Depends(get_session)):
    """
    Add user as coach of the given edition
    """

    logic.add_coach(db, user_id, edition_id)
