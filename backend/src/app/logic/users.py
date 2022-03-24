from sqlalchemy.orm import Session

from src.app.schemas.users import UsersListResponse, AdminPatch
import src.database.crud.users as users_crud


def get_users_list(db: Session, admin: bool, edition_id: int | None) -> UsersListResponse:
    """
    Query the database for a list of users
    and wrap the result in a pydantic model
    """

    if admin:
        if edition_id is None:
            users_orm = users_crud.get_all_admins(db)
        else:
            users_orm = users_crud.get_admins_from_edition(db, edition_id)
    else:
        if edition_id is None:
            users_orm = users_crud.get_all_users(db)
        else:
            users_orm = users_crud.get_users_from_edition(db, edition_id)

    return UsersListResponse(users=users_orm)


def edit_admin_status(db: Session, user_id: int, admin: AdminPatch):
    """
    Edit the admin-status of a user
    """

    users_crud.edit_admin_status(db, user_id, admin.admin)


def add_coach(db: Session, user_id: int, edition_id: int):
    """
    Add user as coach for the given edition
    """

    users_crud.add_coach(db, user_id, edition_id)


def remove_coach(db: Session, user_id: int, edition_id: int):
    """
    Remove user as coach for the given edition
    """

    users_crud.remove_coach(db, user_id, edition_id)


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
