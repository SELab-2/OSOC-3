from pydantic import BaseModel


class EditionBase(BaseModel):
    """Schema of an edition

    Args:
        BaseModel (BaseModel): needed to make EditionBase pydantic.
    """
    year: int


class Edition(BaseModel):
    """Schema of an created edition

    Args:
        BaseModel (BaseModel): needed to make EditionBase pydantic.
    """
    edition_id: int
    year: int

    class Config:
        orm_mode = True
