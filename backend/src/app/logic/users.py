from sqlalchemy.orm import Session

from src.app.schemas.users import UsersListResponse, AdminPatch, UserRequestsResponse, UserRequest
import src.database.crud.users as users_crud
from src.database.models import User


def get_users_list(db: Session, admin: bool, edition_name: str | None) -> UsersListResponse:
    """
    Query the database for a list of users
    and wrap the result in a pydantic model
    """

    if admin:
        if edition_name is None:
            users_orm = users_crud.get_all_admins(db)
        else:
            users_orm = users_crud.get_admins_from_edition(db, edition_name)
    else:
        if edition_name is None:
            users_orm = users_crud.get_all_users(db)
        else:
            users_orm = users_crud.get_users_from_edition(db, edition_name)

    return UsersListResponse(users=users_orm)


def get_user_editions(user: User) -> list[str]:
    """Get all names of the editions this user is coach in"""
    return users_crud.get_user_edition_names(user)


def edit_admin_status(db: Session, user_id: int, admin: AdminPatch):
    """
    Edit the admin-status of a user
    """

    users_crud.edit_admin_status(db, user_id, admin.admin)


def add_coach(db: Session, user_id: int, edition_name: str):
    """
    Add user as coach for the given edition
    """

    users_crud.add_coach(db, user_id, edition_name)


def remove_coach(db: Session, user_id: int, edition_name: str):
    """
    Remove user as coach for the given edition
    """

    users_crud.remove_coach(db, user_id, edition_name)


def remove_coach_all_editions(db: Session, user_id: int):
    """
    Remove user as coach from all editions
    """

    users_crud.remove_coach_all_editions(db, user_id)


def get_request_list(db: Session, edition_name: str | None) -> UserRequestsResponse:
    """
    Query the database for a list of all user requests
    and wrap the result in a pydantic model
    """

    if edition_name is None:
        requests = users_crud.get_all_requests(db)
    else:
        requests = users_crud.get_all_requests_from_edition(db, edition_name)

    requests_model = []
    for request in requests:
        user_req = UserRequest(request_id=request.request_id, edition_name=request.edition.name, user=request.user)
        requests_model.append(user_req)
    return UserRequestsResponse(requests=requests_model)


def accept_request(db: Session, request_id: int):
    """
    Accept user request
    """

    users_crud.accept_request(db, request_id)


def reject_request(db: Session, request_id: int):
    """
    Reject user request
    """

    users_crud.reject_request(db, request_id)
