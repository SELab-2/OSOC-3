from src.app.schemas.utils import CamelCaseModel


class User(CamelCaseModel):
    """Model for a user"""

    user_id: int
    name: str
    admin: bool

    class Config:
        """Set to ORM mode"""
        orm_mode = True


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
