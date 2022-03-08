from src.app.schemas.webhooks import WebhookEvent, Question, Form, QuestionOption, QuestionUpload
from src.database.models import Question as QuestionModel, QuestionAnswer, QuestionFileAnswer, Student, Edition
from src.database.enums import QuestionEnum as QE
from settings import FormMapping
from sqlalchemy.orm import Session


# TODO: add edition
def process_webhook(edition: Edition, data: WebhookEvent, db: Session):
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
    print(attributes)
    student: Student = Student(**attributes)

    db.add(student)

    for question in extra_questions:

        if QE(question.type) == QE.CHECKBOXES and not question.options:
            continue

        model = QuestionModel(
            type=question.type,
            question=question.label,
            student=student
        )

        db.add(model)

        print(question)

        match QE(question.type):
            case QE.MULTIPLE_CHOICE:
                value: str = question.value
                for option in question.options:
                    if option.id == value:
                        db.add(QuestionAnswer(
                            answer=option.text,
                            question=model
                        ))
                        break  # Only one answer in multiple choice questions.
            case QE.INPUT_EMAIL | QE.INPUT_LINK | QE.INPUT_TEXT | QE.TEXTAREA | QE.INPUT_PHONE_NUMBER | QE.INPUT_NUMBER:
                if question.value:
                    db.add(QuestionAnswer(
                        answer=question.value,
                        question=model
                    ))
            case QE.FILE_UPLOAD:
                if question.value:
                    for upload in question.value:
                        db.add(QuestionFileAnswer(
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
                            print('.')
                            db.add(QuestionAnswer(
                                answer=option.text,
                                question=model
                            ))
                            #break  # Only one answer per value in checkbox questions.
            case _:
                # TODO: replace with proper handling, preferably just log and don't fail hard.
                raise Exception('Unkown question type')

    db.commit()
