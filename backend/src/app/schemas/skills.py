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
    desc: str