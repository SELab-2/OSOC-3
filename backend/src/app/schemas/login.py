from src.app.schemas.utils import CamelCaseModel


class UserData(CamelCaseModel):
    """User information that can be passed to frontend
    Includes the id's of the editions a user is coach in
    TODO replace with names once id-name change is merged
    """
    admin: bool
    editions: list[int] = []

    class Config:
        orm_mode = True


class Token(CamelCaseModel):
    """Token generated after login
    Also contains data about the User to set permissions in frontend
    """
    access_token: str
    token_type: str
    user: UserData
