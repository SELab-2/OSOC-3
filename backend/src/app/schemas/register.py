from pydantic import validator
from src.app.schemas.webhooks import CamelCaseModel
from src.app.schemas.validators import validate_email_format

class NewUser(CamelCaseModel):
    name: str
    email: str
    pw: str
    
    @validator("email")
    def valid_format(cls, v):
        """Check that the email is of a valid format"""
        validate_email_format(v)
        return v

