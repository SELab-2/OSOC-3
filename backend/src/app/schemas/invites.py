from uuid import UUID

from pydantic import BaseModel, Field


# TODO perhaps use CamelCaseModel? What does it do?
class InviteLink(BaseModel):
    uuid: UUID
    target_email: str = Field(alias="email")
    edition_id: int

    class Config:
        allow_population_by_field_name = True
        orm_mode = True


class InvitesListResponse(BaseModel):
    invite_links: list[InviteLink]
