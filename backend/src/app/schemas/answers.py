from src.app.schemas.utils import CamelCaseModel


class File(CamelCaseModel):
    """question files"""
    filename: str
    mime_type: str
    url: str


class QuestionAndAnswer(CamelCaseModel):
    """question and answer"""
    question: str
    answers: list[str]
    files: list[File]


class Questions(CamelCaseModel):
    """return model of questions"""
    q_and_a: list[QuestionAndAnswer]
