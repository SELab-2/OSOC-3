from src.database.models import Student
from src.app.schemas.answers import Questions


async def gives_question_and_answers(student: Student) -> Questions:
    """test"""
    #student_question: question_model = 



    #questions: list[Question] = []
    # for question in student_questions:
    #    questions.append(question)

    #return Question(type=student_question.type,
    #                question=student_question.question,
    #                answers=student_question.answers,
    #                files=student_question.files)

    # return "test"
    return Questions(questions=student.questions)
