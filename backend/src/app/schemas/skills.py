from src.app.schemas.utils import CamelCaseModel


class SkillBase(CamelCaseModel):
    """Schema of a skill"""
    name: str


class Skill(CamelCaseModel):
    """Schema of a created skill"""
    skill_id: int
    name: str

    class Config:
        """Set to ORM mode"""
        orm_mode = True


class SkillList(CamelCaseModel):
    """A list of Skills"""
    skills: list[Skill]

    class Config:
        """Set to ORM mode"""
        orm_mode = True
