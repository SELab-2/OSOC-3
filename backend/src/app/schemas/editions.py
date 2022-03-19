from src.app.schemas.webhooks import CamelCaseModel


class EditionBase(CamelCaseModel):
    """Schema of an edition"""
    year: int


class Edition(CamelCaseModel):
    """Schema of an created edition"""
    edition_id: int
    year: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class EditionList(CamelCaseModel):
    """A list of editions"""
    editions: list[Edition]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
