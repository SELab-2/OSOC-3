from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from starlette import status

import src.app.logic.users as logic
from src.app.routers.tags import Tags
from src.app.schemas.login import UserData
from src.app.schemas.users import UsersListResponse, AdminPatch, UserRequestsResponse, user_model_to_schema, \
    FilterParameters
from src.app.utils.dependencies import require_admin, get_user_from_access_token
from src.database.database import get_session
from src.database.models import User as UserDB

users_router = APIRouter(prefix="/users", tags=[Tags.USERS])


@users_router.get("", response_model=UsersListResponse, dependencies=[Depends(require_admin)])
async def get_users(
        params: FilterParameters = Depends(),
        db: Session = Depends(get_session)):
    """
    Get users

    When the admin parameter is True, the edition and exclude_edition parameter will have no effect.
    Since admins have access to all editions.
    """
    return logic.get_users_list(db, params)


@users_router.get("/current", response_model=UserData)
async def get_current_user(db: Session = Depends(get_session), user: UserDB = Depends(get_user_from_access_token)):
    """Get a user based on their authorization credentials"""
    user_data = user_model_to_schema(user).__dict__
    user_data["editions"] = logic.get_user_editions(db, user)

    return user_data


@users_router.patch("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_admin)])
async def patch_admin_status(user_id: int, admin: AdminPatch, db: Session = Depends(get_session)):
    """
    Set admin-status of user
    """
    logic.edit_admin_status(db, user_id, admin)


@users_router.post("/{user_id}/editions/{edition_name}", status_code=status.HTTP_204_NO_CONTENT,
                   dependencies=[Depends(require_admin)])
async def add_to_edition(user_id: int, edition_name: str, db: Session = Depends(get_session)):
    """
    Add user as coach of the given edition
    """
    logic.add_coach(db, user_id, edition_name)


@users_router.delete("/{user_id}/editions/{edition_name}", status_code=status.HTTP_204_NO_CONTENT,
                     dependencies=[Depends(require_admin)])
async def remove_from_edition(user_id: int, edition_name: str, db: Session = Depends(get_session)):
    """
    Remove user as coach of the given edition
    """
    logic.remove_coach(db, user_id, edition_name)


@users_router.delete("/{user_id}/editions", status_code=status.HTTP_204_NO_CONTENT,
                     dependencies=[Depends(require_admin)])
async def remove_from_all_editions(user_id: int, db: Session = Depends(get_session)):
    """
    Remove user as coach from all editions
    """
    logic.remove_coach_all_editions(db, user_id)


@users_router.get("/requests", response_model=UserRequestsResponse, dependencies=[Depends(require_admin)])
async def get_requests(
        edition: str | None = Query(None),
        user: str | None = Query(None),
        page: int = 0,
        db: Session = Depends(get_session)):
    """
    Get pending userrequests
    """
    return logic.get_request_list(db, edition, user, page)


@users_router.post("/requests/{request_id}/accept", status_code=status.HTTP_204_NO_CONTENT,
                   dependencies=[Depends(require_admin)])
async def accept_request(request_id: int, db: Session = Depends(get_session)):
    """
    Accept a coach request
    """
    logic.accept_request(db, request_id)


@users_router.post("/requests/{request_id}/reject", status_code=status.HTTP_204_NO_CONTENT,
                   dependencies=[Depends(require_admin)])
async def reject_request(request_id: int, db: Session = Depends(get_session)):
    """
    Reject a coach request
    """
    logic.reject_request(db, request_id)
