from src.app.schemas.utils import CamelCaseModel
from src.database.models import User as ModelUser


class User(CamelCaseModel):
    """Model for a user"""

    user_id: int
    name: str
    admin: bool
    auth_type: str | None
    email: str | None

    class Config:
        """Set to ORM mode"""
        orm_mode = True


def user_model_to_schema(model_user: ModelUser) -> User:
    auth_type: str | None = None
    email: str | None = None
    if model_user.email_auth is not None:
        auth_type = "email"
        email = model_user.email_auth.email
    elif model_user.github_auth is not None:
        auth_type = "github"
        email = model_user.github_auth.email
    elif model_user.google_auth is not None:
        auth_type = "google"
        email = model_user.google_auth.email

    return User(
        user_id=model_user.user_id,
        name=model_user.name,
        admin=model_user.admin,
        auth_type=auth_type,
        email=email)


class UsersListResponse(CamelCaseModel):
    """Model for a list of users"""

    users: list[User]


class AdminPatch(CamelCaseModel):
    """Body of a patch to change the admin status of a user"""

    admin: bool


class UserRequest(CamelCaseModel):
    """Model for a userrequest"""

    request_id: int
    edition_name: str
    user: User

    class Config:
        """Set to ORM mode"""
        orm_mode = True


class UserRequestsResponse(CamelCaseModel):
    """Model for a list of userrequests"""

    requests: list[UserRequest]
