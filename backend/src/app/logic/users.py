from sqlalchemy.orm import Session

import src.database.crud.users as users_crud
from src.app.schemas.users import UsersListResponse, AdminPatch, UserRequestsResponse, UserRequest, user_model_to_schema
from src.database.models import User


def get_users_list(
        db: Session,
        admin: bool | None,
        edition_name: str | None,
        exclude_edition: str | None,
        name: str | None,
        page: int
) -> UsersListResponse:
    """
    Query the database for a list of users
    and wrap the result in a pydantic model
    """

    users_orm = users_crud.get_users_filtered(db, admin, edition_name, exclude_edition, name, page)

    users = []
    for user in users_orm:
        users.append(user_model_to_schema(user))
    return UsersListResponse(users=users)


def get_user_editions(db: Session, user: User) -> list[str]:
    """Get all names of the editions this user is coach in"""
    return users_crud.get_user_edition_names(db, user)


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


def get_request_list(db: Session, edition_name: str | None, user_name: str | None, page: int) -> UserRequestsResponse:
    """
    Query the database for a list of all user requests
    and wrap the result in a pydantic model
    """

    if user_name is None:
        user_name = ""

    if edition_name is None:
        requests = users_crud.get_requests_page(db, page, user_name)
    else:
        requests = users_crud.get_requests_for_edition_page(db, edition_name, page, user_name)

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
