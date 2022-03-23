
from src.app.schemas.webhooks import CamelCaseModel


class User(CamelCaseModel):
    """Model for a user"""

    user_id: int
    name: str
    email: str
    admin: bool

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class UsersListResponse(CamelCaseModel):
    """Model for a list of users"""

    users: list[User]


class AdminPatch(CamelCaseModel):
    """Body of a patch to change the admin status of a user"""

    admin: bool


class UserRequest(CamelCaseModel):
    """Model for a userrequest"""

    request_id: int
    edition_id: int
    user: User

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class UserRequestsResponse(CamelCaseModel):
    """Model for a list of userrequests"""

    requests: list[UserRequest]
