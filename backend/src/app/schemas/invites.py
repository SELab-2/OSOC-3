from uuid import UUID

from pydantic import Field, validator

from src.app.schemas.validators import validate_email_format
from src.app.schemas.utils import CamelCaseModel


class EmailAddress(CamelCaseModel):
    """Model for email addresses
    Performs basic validation through a regex
    """
    email: str

    @validator("email")
    def valid_format(cls, validate):
        """Check that the email is of a valid format"""
        validate_email_format(validate)
        return validate


class InviteLink(CamelCaseModel):
    """Model to represent an InviteLink
    Sent as a response to API /GET requests
    """
    invite_link_id: int = Field(alias="id")
    uuid: UUID
    target_email: str = Field(alias="email")
    edition_name: str

    class Config:
        """Set to ORM mode"""
        orm_mode = True


class InvitesLinkList(CamelCaseModel):
    """A list of invite link models
    Sending a pure list as JSON is bad practice, lists should be wrapped in
    a dict with 1 key that leads to them instead. This class handles that.
    """
    invite_links: list[InviteLink]


class NewInviteLink(CamelCaseModel):
    """A response containing a mailto link to invite a user with
    Also contains the regular link in case the user wants to invite manually
    """
    mail_to: str
    invite_link: str
