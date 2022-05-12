from src.database.models import Student
from src.app.schemas.answers import Questions


async def gives_question_and_answers(student: Student) -> Questions:
    """transfers the student questions into a return model of Questions"""
    return Questions(questions=student.questions)
