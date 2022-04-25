from pydantic import validator, BaseModel

from src.app.exceptions.validation_exception import ValidationException


class AccessTokenResponse(BaseModel):
    """Model for the response sent by GitHub when we request a user's access token"""
    access_token: str
    scope: str

    @validator("scope")
    @classmethod
    def split_scope(cls, scopes: str) -> str:
        """Check if all the required scopes are present (users can deny them if they want to)"""
        required_scopes = ["read:user", "user:email"]
        provided_scopes = scopes.split(",")

        if not all(scope in provided_scopes for scope in required_scopes):
            raise ValidationException("Missing scopes")

        return scopes


class GitHubProfile(BaseModel):
    """Model for data we have about a user's GitHub profile"""
    access_token: str
    email: str
    id: int
    name: str
