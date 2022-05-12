import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database.models import Edition, User, Skill, Student, Question, QuestionAnswer
from src.database.enums import QuestionEnum
from tests.utils.authorization import AuthClient


@pytest.fixture
async def database_with_data(database_session: AsyncSession) -> AsyncSession:
    """fixture for adding data to the database"""
    edition: Edition = Edition(year=2022, name="ed2022")
    database_session.add(edition)
    user: User = User(name="coach1")
    database_session.add(user)
    skill1: Skill = Skill(name="skill1", description="something about skill1")
    skill2: Skill = Skill(name="skill2", description="something about skill2")
    skill3: Skill = Skill(name="skill3", description="something about skill3")
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
        type=QuestionEnum.INPUT_EMAIL, question="Email", student=student01, answers=[], files=[])
    database_session.add(question1)
    question_answer1: QuestionAnswer = QuestionAnswer(
        answer="josvermeulen@mail.com", question=question1)
    database_session.add(question_answer1)

    #aswer1: QuestionAnswer = QuestionAnswer(answer="josvermeulen@mail.com", question=question1)
    # database_session.add(aswer1)
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


async def test_get_answers_as_coach(database_with_data: AsyncSession, auth_client: AuthClient, current_edition: Edition):
    """test get answers when logged in as coach"""
    await auth_client.coach(current_edition)
    async with auth_client:
        response = await auth_client.get("/editions/ed2023/students/1/answers", follow_redirects=True)
        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert len(json["questions"]) == 1
        assert QuestionEnum(json["questions"][0]["type"]
                            ) == QuestionEnum.INPUT_EMAIL
        assert json["questions"][0]["question"] == "Email"
        assert len(json["questions"][0]["answers"]) == 1
        assert json["questions"][0]["answers"][0]["answer"] == "josvermeulen@mail.com"
        assert len(json["questions"][0]["files"]) == 0


async def test_get_answers_as_admin(database_with_data: AsyncSession, auth_client: AuthClient):
    """test get answers when logged in as admin"""
    await auth_client.admin()
    async with auth_client:
        response = await auth_client.get("/editions/ed2023/students/1/answers", follow_redirects=True)
        assert response.status_code == status.HTTP_200_OK
        json = response.json()
        assert len(json["questions"]) == 1
        assert QuestionEnum(json["questions"][0]["type"]
                            ) == QuestionEnum.INPUT_EMAIL
        assert json["questions"][0]["question"] == "Email"
        assert len(json["questions"][0]["answers"]) == 1
        assert json["questions"][0]["answers"][0]["answer"] == "josvermeulen@mail.com"
        assert len(json["questions"][0]["files"]) == 0
