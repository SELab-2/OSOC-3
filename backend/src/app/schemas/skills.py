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


class SkillBase(CamelCaseModel):
    """Schema of a skill

    Args:
        CamelCaseModel (CamelCaseModel): needed to make SkillBase pydantic.
    """
    name: str
    description: str


class Skill(CamelCaseModel):
    """Schema of a created skill

    Args:
        CamelCaseModel (CamelCaseModel): needed to make SkillBase pydantic.
    """
    skill_id: int
    name: str
    description: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class SkillList(CamelCaseModel):
    """A list of Skills

    Args:
        CamelCaseModel (CamelCaseModel): needed to make SkillList pydantic.
    """
    skills: list[Skill]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True