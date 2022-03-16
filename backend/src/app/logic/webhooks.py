import sqlalchemy.exc
from sqlalchemy.orm import Session

from settings import FormMapping
from src.app.exceptions.webhooks import WebhookProcessException
from src.app.schemas.webhooks import WebhookEvent, Question, Form
from src.database.enums import QuestionEnum as QE
from src.database.models import Question as QuestionModel, QuestionAnswer, QuestionFileAnswer, Student, Edition


def process_webhook(edition: Edition, data: WebhookEvent, database: Session):
    """
    Process webhook data

    Given a form process all required question and save remaining in a generic question table.
    """
    form: Form = data.data
    questions: list[Question] = form.fields
    extra_questions: list[Question] = []

    attributes: dict[str, str | int] = {'edition': edition}

    for question in questions:
        question: Question
        match FormMapping(question.key):
            case FormMapping.FIRST_NAME:
                attributes['first_name'] = question.value
            case FormMapping.LAST_NAME:
                attributes['last_name'] = question.value
            case FormMapping.PREFERRED_NAME:
                attributes['preferred_name'] = question.value
            case FormMapping.EMAIL:
                attributes['email_address'] = question.value
            case FormMapping.PHONE_NUMBER:
                attributes['phone_number'] = question.value
            case FormMapping.STUDENT_COACH:
                for option in question.options:
                    if option.id == question.value:
                        attributes['wants_to_be_student_coach'] = "yes" in option.text.lower()
                        break  # Only 2 options, Yes and No.
            case _:
                extra_questions.append(question)

    # Check all attributes are included and not None
    needed = {
        'first_name',
        'last_name',
        'preferred_name',
        'email_address',
        'phone_number',
        'wants_to_be_student_coach',
        'edition'
    }

    diff = set(attributes.keys()).symmetric_difference(needed)
    if len(diff) != 0:
        raise WebhookProcessException(f'Missing questions for Attributes {diff}')

    student: Student = Student(**attributes)

    database.add(student)

    process_remaining_questions(student, extra_questions, database)

    try:
        database.commit()
    except sqlalchemy.exc.IntegrityError as error:
        raise WebhookProcessException('Unique Check Failed') from error


def process_remaining_questions(student: Student, questions: list[Question], database: Session):
    """Process all remaining questions"""
    for question in questions:

        if QE(question.type) == QE.CHECKBOXES and not question.options:
            continue

        model = QuestionModel(
            type=question.type,
            question=question.label,
            student=student
        )

        database.add(model)

        match QE(question.type):
            case QE.MULTIPLE_CHOICE:
                value: str = question.value
                for option in question.options:
                    if option.id == value:
                        database.add(QuestionAnswer(
                            answer=option.text,
                            question=model
                        ))
                        break  # Only one answer in multiple choice questions.
            case QE.INPUT_EMAIL | QE.INPUT_LINK | QE.INPUT_TEXT | QE.TEXTAREA | QE.INPUT_PHONE_NUMBER | QE.INPUT_NUMBER:
                if question.value:
                    database.add(QuestionAnswer(
                        answer=question.value,
                        question=model
                    ))
            case QE.FILE_UPLOAD:
                if question.value:
                    for upload in question.value:
                        database.add(QuestionFileAnswer(
                            file_name=upload.name,
                            url=upload.url,
                            mime_type=upload.mime_type,
                            size=upload.size,
                            question=model
                        ))
            case QE.CHECKBOXES:
                for value in question.value:
                    for option in question.options:
                        if option.id == value:
                            database.add(QuestionAnswer(
                                answer=option.text,
                                question=model
                            ))
            case _:
                raise WebhookProcessException('Unknown question type')
