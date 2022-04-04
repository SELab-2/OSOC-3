from pydantic import validator

from src.app.schemas.utils import CamelCaseModel
from src.app.schemas.validators import validate_edition


class EditionBase(CamelCaseModel):
    """Schema of an edition"""
    name: str
    year: int

    @validator("name")
    def valid_format(cls, v):
        """Check that the email is of a valid format"""
        validate_edition(v)
        return v


class Edition(CamelCaseModel):
    """Schema of a created edition"""
    edition_id: int
    name: str
    year: int

    class Config:
        """Set to ORM mode"""
        orm_mode = True


class EditionList(CamelCaseModel):
    """A list of editions"""
    editions: list[Edition]

    class Config:
        """Set to ORM mode"""
        orm_mode = True
