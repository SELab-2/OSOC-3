from src.app.schemas.editions import Edition
from src.app.schemas.users import User
from src.app.schemas.utils import BaseModel


class UserData(User):
    """User information that can be passed to frontend"""
    editions: list[Edition] = []


class Token(BaseModel):
    """Token generated after login
    Also contains data about the User to set permissions in frontend
    """
    access_token: str
    refresh_token: str
    token_type: str
    user: UserData
