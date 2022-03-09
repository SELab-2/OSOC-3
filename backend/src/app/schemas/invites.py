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


class InviteLink(CamelCaseModel):
    uuid: UUID
    target_email: str = Field(alias="email")
    edition_id: int

    class Config:
        allow_population_by_field_name = True
        orm_mode = True


class InvitesListResponse(CamelCaseModel):
    invite_links: list[InviteLink]
