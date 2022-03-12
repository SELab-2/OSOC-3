from pydantic import BaseModel
from humps import camelize


def to_camel(string: str) -> str:
    return camelize(string)


class CamelCaseModel(BaseModel):
    """ To have camel-case JSON request/response body while keeping the models snake-cased

    Args:
        BaseModel (BaseModel): needed to make the CamelCaseModel pydantic
    """
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class EditionBase(CamelCaseModel):
    """Schema of an edition

    Args:
        CamelCaseModel (CamelCaseModel): needed to make EditionBase pydantic.
    """
    year: int


class Edition(CamelCaseModel):
    """Schema of an created edition

    Args:
        CamelCaseModel (CamelCaseModel): needed to make EditionBase pydantic.
    """
    edition_id: int
    year: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class EditionList(CamelCaseModel):
    """A list of editions

    Args:
        CamelCaseModel (CamelCaseModel): needed to make EditionList pydantic.
    """
    editions: list[Edition]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True