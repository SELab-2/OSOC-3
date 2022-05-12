from src.app.schemas.utils import CamelCaseModel
from src.database.enums import QuestionEnum


class QuestionAnswer(CamelCaseModel):
    """test"""
    answer: str

    class Config:
        """Set to ORM mode"""
        orm_mode = True


class QuestionFileAnswer(CamelCaseModel):
    """test"""
    file_name: str
    url: str
    mime_type: str
    size: str

    class Config:
        """Set to ORM mode"""
        orm_mode = True


class Question(CamelCaseModel):
    """test"""
    type: QuestionEnum
    question: str
    answers: list[QuestionAnswer]
    files: list[QuestionFileAnswer]

    class Config:
        """Set to ORM mode"""
        orm_mode = True


class Questions(CamelCaseModel):
    """test"""
    questions: list[Question]

    class Config:
        """Set to ORM mode"""
        orm_mode = True
