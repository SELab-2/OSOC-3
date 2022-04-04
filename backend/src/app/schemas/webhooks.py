from typing import Optional
from uuid import UUID

from humps import camelize
from pydantic import BaseModel


def to_camel(string: str) -> str:
    """Return the camel case version of a given string"""
    return camelize(string)


class CamelCaseModel(BaseModel):
    """Base model that converts snake to camel case when serialized"""
    class Config:
        """Config"""
        alias_generator = to_camel
        allow_population_by_field_name = True


class QuestionOption(CamelCaseModel):
    """Options for a question"""
    id: str
    text: str


class QuestionUpload(CamelCaseModel):
    """Model representing a file upload"""
    name: str
    url: str
    mime_type: str
    size: int


class Question(CamelCaseModel):
    """Model representing a Question of the form"""
    key: str
    label: str
    type: str
    value: str | list[QuestionUpload] | list[str] | int | None
    options: Optional[list[QuestionOption]]


class Form(CamelCaseModel):
    """The form data containing all the questions"""
    response_id: str
    submission_id: str
    form_id: str
    form_name: str
    created_at: str
    fields: list[Question]


class WebhookEvent(CamelCaseModel):
    """The webhook event holding the form data"""
    event_id: str
    created_at: str
    data: Form


class WebhookUrlResponse(BaseModel):
    """Response model to return a webhook url uuid"""
    uuid: UUID

    class Config:
        """Config"""
        orm_mode = True
