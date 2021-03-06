from pydantic import validator

from src.app.schemas.utils import CamelCaseModel
from src.app.schemas.validators import validate_edition


class EditionBase(CamelCaseModel):
    """Schema of an edition"""
    name: str
    year: int

    @validator("name")
    @classmethod
    def valid_format(cls, value):
        """Check that the edition name is of a valid format"""
        validate_edition(value)
        return value


class Edition(CamelCaseModel):
    """Schema of a created edition"""
    edition_id: int
    name: str
    year: int
    readonly: bool

    class Config:
        """Set to ORM mode"""
        orm_mode = True


class EditionList(CamelCaseModel):
    """A list of editions"""
    editions: list[Edition]

    class Config:
        """Set to ORM mode"""
        orm_mode = True


class EditEdition(CamelCaseModel):
    """Input schema to edit an edition
    Only supported operation is patching the readonly status
    """
    readonly: bool
