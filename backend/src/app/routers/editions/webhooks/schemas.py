from typing import Optional
from uuid import UUID

from humps import camelize
from pydantic import BaseModel


def to_camel(string: str) -> str:
    return camelize(string)


class CamelCaseModel(BaseModel):
    class Config:
        alias_generator = to_camel


class QuestionOption(CamelCaseModel):
    id: str
    text: str


class QuestionUpload(CamelCaseModel):
    name: str
    url: str
    mime_type: str
    size: int


class Question(CamelCaseModel):
    key: str
    label: str
    type: str
    value: str | list[QuestionUpload] | list[str] | int
    options: Optional[list[QuestionOption]]


class Form(CamelCaseModel):
    response_id: str
    submission_id: str
    response_id: str
    form_id: str
    form_name: str
    created_at: str
    fields: list[Question]


class WebhookEvent(CamelCaseModel):
    event_id: str
    created_at: str
    data: Form


class WebhookUrlResponse(BaseModel):
    uuid: UUID
