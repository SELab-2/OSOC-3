from src.database.models import Student
from src.app.schemas.answers import Questions, QuestionAndAnswer, File


async def gives_question_and_answers(student: Student) -> Questions:
    """transfers the student questions into a return model of Questions"""
    # return Questions(questions=student.questions)
    q_and_as: list[QuestionAndAnswer] = []
    for question in student.questions:
        answers: list[str] = []
        for answer in question.answers:
            answers.append(answer.answer)

        files: list[File] = []
        for file in question.files:
            files.append(File(filename=file.file_name,
                         mime_type=file.mime_type, url=file.url))

        q_and_as.append(QuestionAndAnswer(
            question=question.question, answers=answers, files=files))
    return Questions(q_and_a=q_and_as)
