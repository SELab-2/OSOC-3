
from src.app.schemas.webhooks import CamelCaseModel


class User(CamelCaseModel):
    user_id: int
    name: str
    email: str
    admin: bool

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class UsersListResponse(CamelCaseModel):
    users: list[User]


class AdminPatch(CamelCaseModel):
    admin: bool

class RequestAnswer(CamelCaseModel):
    accept: bool


