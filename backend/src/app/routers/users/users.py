from fastapi import APIRouter, Query, Depends
from requests import Session

from src.app.routers.tags import Tags
import src.app.logic.users as logic
from src.app.schemas.users import UsersListResponse, AdminPatch, UserRequestsResponse, User as UserSchema
from src.app.utils.dependencies import require_admin, get_current_active_user
from src.database.database import get_session
from src.database.models import User as UserDB

users_router = APIRouter(prefix="/users", tags=[Tags.USERS])


@users_router.get("/", response_model=UsersListResponse, dependencies=[Depends(require_admin)])
async def get_users(admin: bool = Query(False), edition: str | None = Query(None), db: Session = Depends(get_session)):
    """
    Get users
    """

    return logic.get_users_list(db, admin, edition)


@users_router.get("/current", response_model=UserSchema)
async def get_current_user(user: UserDB = Depends(get_current_active_user)):
    """Get a user based on their authorization credentials"""
    return user


@users_router.patch("/{user_id}", status_code=204, dependencies=[Depends(require_admin)])
async def patch_admin_status(user_id: int, admin: AdminPatch, db: Session = Depends(get_session)):
    """
    Set admin-status of user
    """

    logic.edit_admin_status(db, user_id, admin)


@users_router.post("/{user_id}/editions/{edition_name}", status_code=204, dependencies=[Depends(require_admin)])
async def add_to_edition(user_id: int, edition_name: str, db: Session = Depends(get_session)):
    """
    Add user as coach of the given edition
    """

    logic.add_coach(db, user_id, edition_name)


@users_router.delete("/{user_id}/editions/{edition_name}", status_code=204, dependencies=[Depends(require_admin)])
async def remove_from_edition(user_id: int, edition_name: str, db: Session = Depends(get_session)):
    """
    Remove user as coach of the given edition
    """

    logic.remove_coach(db, user_id, edition_name)


@users_router.get("/requests", response_model=UserRequestsResponse, dependencies=[Depends(require_admin)])
async def get_requests(edition: str | None = Query(None), db: Session = Depends(get_session)):
    """
    Get pending userrequests
    """

    return logic.get_request_list(db, edition)


@users_router.post("/requests/{request_id}/accept", status_code=204, dependencies=[Depends(require_admin)])
async def accept_request(request_id: int, db: Session = Depends(get_session)):
    """
    Accept a coach request
    """

    logic.accept_request(db, request_id)


@users_router.post("/requests/{request_id}/reject", status_code=204, dependencies=[Depends(require_admin)])
async def reject_request(request_id: int, db: Session = Depends(get_session)):
    """
    Reject a coach request
    """

    logic.reject_request(db, request_id)
