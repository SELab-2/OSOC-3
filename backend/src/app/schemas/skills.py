from pydantic import BaseModel


class SkillBase(BaseModel):
    """Schema of a skill

    Args:
        BaseModel (BaseModel): needed to make SkillBase pydantic.
    """
    name: str
    desc: str