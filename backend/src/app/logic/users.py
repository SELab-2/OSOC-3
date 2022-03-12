from sqlalchemy.orm import Session

from src.app.schemas.users import UsersListResponse
from src.database.crud.users import get_users_from_edition


def get_users_list(db: Session, edition: int) -> UsersListResponse:
    """
    Query the database for a list of users
    and wrap the result in a pydantic model
    """
    users_orm = get_users_from_edition(db, edition)
    return UsersListResponse(users=users_orm)


