from src.app.schemas.utils import CamelCaseModel
from src.database.enums import QuestionEnum


class QuestionAnswer(CamelCaseModel):
    """return model of an answer"""
    answer: str

    class Config:
        """Set to ORM mode"""
        orm_mode = True


class QuestionFileAnswer(CamelCaseModel):
    """return model of a file answers"""
    file_name: str
    url: str
    mime_type: str
    size: str

    class Config:
        """Set to ORM mode"""
        orm_mode = True


class Question(CamelCaseModel):
    """return model of a question"""
    type: QuestionEnum
    question: str
    answers: list[QuestionAnswer]
    files: list[QuestionFileAnswer]

    class Config:
        """Set to ORM mode"""
        orm_mode = True


class Questions(CamelCaseModel):
    """return model of questions"""
    questions: list[Question]

    class Config:
        """Set to ORM mode"""
        orm_mode = True
