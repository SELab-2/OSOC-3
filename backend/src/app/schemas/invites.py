from uuid import UUID

from pydantic import Field, validator

from src.app.schemas.validators import validate_email_format
from src.app.schemas.webhooks import CamelCaseModel


class EmailAddress(CamelCaseModel):
    email: str

    @validator("email")
    def valid_format(cls, v):
        """Check that the email is of a valid format"""
        validate_email_format(v)
        return v


class InviteLink(CamelCaseModel):
    invite_link_id: int = Field(alias="id")
    uuid: UUID
    target_email: str = Field(alias="email")
    edition_id: int

    class Config:
        orm_mode = True


class InvitesListResponse(CamelCaseModel):
    """A list of invite link models
    Sending a pure list as JSON is bad practice, lists should be wrapped in
    a dict with 1 key that leads to them instead. This class handles that.
    """
    invite_links: list[InviteLink]


class MailtoLink(CamelCaseModel):
    """A response containing a mailto link to invite a user with"""
    mail_to: str
