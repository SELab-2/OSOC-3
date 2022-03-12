from sqlalchemy.orm import Session

from src.app.schemas.users import UsersListResponse, Status, RequestAnswer
import src.database.crud.users as users_crud
from src.database.enums import RoleEnum


def get_users_list(db: Session, edition: int) -> UsersListResponse:
    """
    Query the database for a list of users
    and wrap the result in a pydantic model
    """

    users_orm = users_crud.get_users_from_edition(db, edition)
    return UsersListResponse(users=users_orm)


def add_user_as_coach(db: Session, edition_id: int, user_id: int):
    """
    Add user as admin for the given edition if not already coach
    """

    users_crud.add_user_as_coach(db, edition_id, user_id)


def delete_user_as_coach(db: Session, edition_id: int, user_id: int):
    """
    Add user as admin for the given edition if not already coach
    """

    users_crud.delete_user_as_coach(db, edition_id, user_id)


def handle_user_request(db: Session, edition_id: int, user_id: int, answer: RequestAnswer):
    """Accept/Reject user request"""

    if answer.accept:
        users_crud.accept_request(db, edition_id, user_id)
    else:
        users_crud.reject_request(db, user_id)
