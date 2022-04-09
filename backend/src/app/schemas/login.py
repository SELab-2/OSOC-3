from src.app.schemas.users import User
from src.app.schemas.utils import CamelCaseModel


class UserData(User):
    """User information that can be passed to frontend"""
    editions: list[str] = []


class Token(CamelCaseModel):
    """Token generated after login
    Also contains data about the User to set permissions in frontend
    """
    access_token: str
    token_type: str
    user: UserData
