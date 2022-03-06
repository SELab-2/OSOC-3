"""
All the database models should be added here
Make sure they inherit the BaseModel class to make them pydantic
"""
from pydantic import BaseModel


class SkillBase(BaseModel):
    """Schema of a skill

    Args:
        BaseModel (BaseModel): needed to make SkillBase pydantic.
    """
    name: str
    desc: str