from typing import Type

from src.app.schemas.editions import Edition
from src.app.schemas.utils import CamelCaseModel, BaseModel
from src.database.models import User as ModelUser


class Authentication(CamelCaseModel):
    """Model for an authentication method"""
    auth_type: str
    email: str


def get_user_model_auth(model_user: ModelUser) -> Authentication | None:
    """Get a user's auth type"""
    auth: Authentication | None = None

    if model_user.email_auth is not None:
        auth = Authentication(auth_type="email", email=model_user.email_auth.email)
    elif model_user.github_auth is not None:
        auth = Authentication(auth_type="github", email=model_user.github_auth.email)
    elif model_user.google_auth is not None:
        auth = Authentication(auth_type="google", email=model_user.google_auth.email)

    return auth


class User(CamelCaseModel):
    """Model for a user"""
    user_id: int
    name: str
    admin: bool
    auth: Authentication | None

    @classmethod
    def from_orm(cls: Type['User'], obj: ModelUser) -> 'User':
        """Override from_orm in order to instantiate the auth field"""
        auth = get_user_model_auth(obj)
        return cls(user_id=obj.user_id, name=obj.name, admin=obj.admin, auth=auth)

    class Config:
        """Set to ORM mode"""
        orm_mode = True


def user_model_to_schema(model_user: ModelUser) -> User:
    """Create User Schema from User Model"""
    auth = get_user_model_auth(model_user)

    return User(
        user_id=model_user.user_id,
        name=model_user.name,
        admin=model_user.admin,
        auth=auth
    )


class UsersListResponse(CamelCaseModel):
    """Model for a list of users"""

    users: list[User]


class AdminPatch(CamelCaseModel):
    """Body of a patch to change the admin status of a user"""

    admin: bool


class UserRequest(CamelCaseModel):
    """Model for a userrequest"""

    request_id: int
    edition: Edition
    user: User

    class Config:
        """Set to ORM mode"""
        orm_mode = True


class UserRequestsResponse(CamelCaseModel):
    """Model for a list of userrequests"""

    requests: list[UserRequest]


class FilterParameters(BaseModel):
    """Schema for query parameters"""
    edition: str | None = None
    exclude_edition: str | None = None
    name: str | None = None
    admin: bool | None = None
    page: int = 0
