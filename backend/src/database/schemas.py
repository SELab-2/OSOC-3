"""
All the database models should be added here
Make sure they inherit the BaseModel class to make them pydantic
"""
from pydantic import BaseModel
from src.database.enums import RoleEnum, DecisionEnum


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


class SkillBase(BaseModel):
    """Schema of a skill

    Args:
        BaseModel (BaseModel): needed to make SkillBase pydantic.
    """
    name: str
    desc: str


class StudentBase(BaseModel):
    """Schema of a student

    Args:
        BaseModel (BaseModel): needed to make StudentBase pydantic.
    """
    name: str
    email_address: str
    phone_number: str
    alumni: bool
    cv_webhook_id: int
    decision: DecisionEnum
    wants_to_be_student_coach: bool