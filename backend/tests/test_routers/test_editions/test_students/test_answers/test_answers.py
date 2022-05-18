import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database.models import Edition, QuestionFileAnswer, User, Skill, Student, Question, QuestionAnswer
from src.database.enums import QuestionEnum
from tests.utils.authorization import AuthClient


@pytest.fixture
async def database_with_data(database_session: AsyncSession) -> AsyncSession:
    """fixture for adding data to the database"""
    edition: Edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    user: User = User(name="coach1")
    database_session.add(user)
    skill1: Skill = Skill(name="skill1")
    skill2: Skill = Skill(name="skill2")
    skill3: Skill = Skill(name="skill3")
    database_session.add(skill1)
    database_session.add(skill2)
    database_session.add(skill3)
    student01: Student = Student(first_name="Jos", last_name="Vermeulen", preferred_name="Joske",
                                 email_address="josvermeulen@mail.com", phone_number="0487/86.24.45", alumni=True,
                                 wants_to_be_student_coach=True, edition=edition, skills=[skill1, skill3])
    student02: Student = Student(first_name="Isabella", last_name="Christensen", preferred_name="Isabella",
                                 email_address="isabella.christensen@example.com", phone_number="98389723", alumni=True,
                                 wants_to_be_student_coach=True, edition=edition, skills=[skill2])
    database_session.add(student01)
    database_session.add(student02)
    question1: Question = Question(
        type=QuestionEnum.INPUT_TEXT, question="Tell me something", student=student01, answers=[], files=[])
    question2: Question = Question(
        type=QuestionEnum.MULTIPLE_CHOICE, question="Favorite drink", student=student01, answers=[], files=[])
    database_session.add(question1)
    database_session.add(question2)
    question_answer1: QuestionAnswer = QuestionAnswer(
        answer="I like pizza", question=question1)
    question_answer2: QuestionAnswer = QuestionAnswer(
        answer="ICE TEA", question=question2)
    question_answer3: QuestionAnswer = QuestionAnswer(
        answer="Cola", question=question2)
    database_session.add(question_answer1)
    database_session.add(question_answer2)
    database_session.add(question_answer3)
    question_file_answer: QuestionFileAnswer = QuestionFileAnswer(
        file_name="pizza.txt", url="een/link/naar/pizza.txt", mime_type="text/plain", size=16, question=question1
    )
    database_session.add(question_file_answer)
    await database_session.commit()
    return database_session


@pytest.fixture
async def current_edition(database_with_data: AsyncSession) -> Edition:
    """fixture to get the latest edition"""
    return (await database_with_data.execute(select(Edition))).scalars().all()[-1]


async def test_get_answers_not_logged_in(database_with_data: AsyncSession, auth_client: AuthClient):
    """test get answers when not logged in"""
    async with auth_client:
        response = await auth_client.get("/editions/ed2023/students/1/answers", follow_redirects=True)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_get_answers_as_coach(database_with_data: AsyncSession, auth_client: AuthClient,
                                    current_edition: Edition):
    """test get answers when logged in as coach"""
    await auth_client.coach(current_edition)
    async with auth_client:
        response = await auth_client.get("/editions/ed2023/students/1/answers", follow_redirects=True)
        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert len(json["qAndA"]) == 2
        assert json["qAndA"][0]["question"] == "Tell me something"
        assert len(json["qAndA"][0]["answers"]) == 1
        assert json["qAndA"][0]["answers"][0] == "I like pizza"
        assert len(json["qAndA"][0]["files"]) == 1
        assert json["qAndA"][0]["files"][0]["filename"] == "pizza.txt"
        assert json["qAndA"][0]["files"][0]["mimeType"] == "text/plain"
        assert json["qAndA"][0]["files"][0]["url"] == "een/link/naar/pizza.txt"
        assert json["qAndA"][1]["question"] == "Favorite drink"
        assert len(json["qAndA"][1]["answers"]) == 2
        assert json["qAndA"][1]["answers"][0] == "ICE TEA"
        assert json["qAndA"][1]["answers"][1] == "Cola"
        assert len(json["qAndA"][1]["files"]) == 0


async def test_get_answers_as_admin(database_with_data: AsyncSession, auth_client: AuthClient):
    """test get answers when logged in as coach"""
    await auth_client.admin()
    async with auth_client:
        response = await auth_client.get("/editions/ed2023/students/1/answers", follow_redirects=True)
        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert len(json["qAndA"]) == 2
        assert json["qAndA"][0]["question"] == "Tell me something"
        assert len(json["qAndA"][0]["answers"]) == 1
        assert json["qAndA"][0]["answers"][0] == "I like pizza"
        assert len(json["qAndA"][0]["files"]) == 1
        assert json["qAndA"][0]["files"][0]["filename"] == "pizza.txt"
        assert json["qAndA"][0]["files"][0]["mimeType"] == "text/plain"
        assert json["qAndA"][0]["files"][0]["url"] == "een/link/naar/pizza.txt"
        assert json["qAndA"][1]["question"] == "Favorite drink"
        assert len(json["qAndA"][1]["answers"]) == 2
        assert json["qAndA"][1]["answers"][0] == "ICE TEA"
        assert json["qAndA"][1]["answers"][1] == "Cola"
        assert len(json["qAndA"][1]["files"]) == 0
