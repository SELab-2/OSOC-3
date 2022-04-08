from src.app.schemas.utils import CamelCaseModel


class UserData(CamelCaseModel):
    """User information that can be passed to frontend
    Includes the names of the editions a user is coach in
    """
    admin: bool
    editions: list[str] = []

    class Config:
        """The Model config"""
        orm_mode = True


class Token(CamelCaseModel):
    """Token generated after login
    Also contains data about the User to set permissions in frontend
    """
    access_token: str
    token_type: str
    user: UserData
