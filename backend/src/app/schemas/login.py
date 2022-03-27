from src.app.schemas.utils import CamelCaseModel


class Token(CamelCaseModel):
    """Token generated after login"""
    access_token: str
    token_type: str


class User(CamelCaseModel):
    """The fields used to find a user in the DB"""
    user_id: int
