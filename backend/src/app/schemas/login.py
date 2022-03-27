from src.app.schemas.utils import CamelCaseModel


class Token(CamelCaseModel):
    """Token generated after login"""
    access_token: str
    token_type: str

    class Config:
        allow_population_by_field_name = True


class User(CamelCaseModel):
    """The fields used to find a user in the DB"""
    user_id: int

    class Config:
        allow_population_by_field_name = True
