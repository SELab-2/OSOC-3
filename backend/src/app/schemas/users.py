from pydantic import BaseModel

from src.app.schemas.webhooks import CamelCaseModel
from src.database.enums import RoleEnum


class User(CamelCaseModel):
    user_id: int
    name: str
    email: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class UsersListResponse(CamelCaseModel):
    users: list[User]


class StatusBody(CamelCaseModel):
    status: RoleEnum
