from src.app.schemas.utils import CamelCaseModel


class SkillBase(CamelCaseModel):
    """Schema of a skill"""
    name: str
    description: str | None = None


class Skill(CamelCaseModel):
    """Schema of a created skill"""
    skill_id: int
    name: str
    description: str | None = None

    class Config:
        orm_mode = True


class SkillList(CamelCaseModel):
    """A list of Skills"""
    skills: list[Skill]

    class Config:
        orm_mode = True
