from sqlalchemy.orm import Session

from src.app.schemas.users import UsersListResponse, StatusBody, Status
import src.database.crud.users as users_crud
from src.database.enums import RoleEnum


def get_users_list(db: Session, edition: int) -> UsersListResponse:
    """
    Query the database for a list of users
    and wrap the result in a pydantic model
    """

    users_orm = users_crud.get_users_from_edition(db, edition)
    return UsersListResponse(users=users_orm)


def update_user_status(db: Session, edition_id: int, user_id: int, status: Status):
    """Change the status of a given user in an edition"""

    # Create db entry
    status = {Status.DISABLED: RoleEnum.DISABLED, Status.ADMIN: RoleEnum.ADMIN, Status.COACH: RoleEnum.COACH}[status]
    users_crud.update_user_status(db, edition_id, user_id, status)
